# Task B — Refactor: Before / After

This is a realistic recreation of the kind of checkout handler described in the
assessment — written by me for this exercise, not lifted from a real employer's
code. It mixes HTTP concerns, pricing logic, inventory mutation, and side effects
in one function, which is the pattern called out in the assessment as Issue 3.

## Before

```javascript
// routes/checkout.js
const express = require('express');
const router = express.Router();
const db = require('../db'); // raw MongoDB client
const stripe = require('stripe')('sk_live_51H8x...'); // hardcoded key

router.post('/checkout', async (req, res) => {
  const { userId, items, couponCode } = req.body;

  let total = 0;
  for (const item of items) {
    const product = await db.collection('products').findOne({ _id: item.productId });
    if (!product) {
      return res.status(400).json({ error: 'Invalid product' });
    }
    if (product.stock < item.quantity) {
      return res.status(400).json({ error: 'Out of stock' });
    }
    total += product.price * item.quantity;
  }

  if (couponCode) {
    const coupon = await db.collection('coupons').findOne({ code: couponCode });
    if (coupon && coupon.expiresAt > new Date()) {
      if (coupon.type === 'percent') {
        total = total - (total * coupon.value / 100);
      } else {
        total = total - coupon.value;
      }
    }
  }

  if (total < 0) total = 0;

  let charge;
  try {
    charge = await stripe.charges.create({
      amount: Math.round(total * 100),
      currency: 'usd',
      source: req.body.stripeToken,
    });
  } catch (err) {
    return res.status(402).json({ error: 'Payment failed' });
  }

  for (const item of items) {
    await db.collection('products').updateOne(
      { _id: item.productId },
      { $inc: { stock: -item.quantity } }
    );
  }

  await db.collection('orders').insertOne({
    userId, items, total, chargeId: charge.id, createdAt: new Date(),
  });

  res.json({ success: true, total });
});

module.exports = router;
```

### What's wrong with this, concretely

- **Secret hardcoded in the file** — the exact issue flagged as Issue 1 in the
  assessment, shown here in context.
- **Pricing, coupon, and inventory logic are unit-testable only by running an
  HTTP server and mocking Express req/res.** There's no way to test "20% coupon
  on a $50 order = $40" without going through the whole route.
- **No transaction boundary.** If the stock decrement loop fails partway through
  (server restart, one bad `productId`), the customer has been charged but stock
  and the order record are inconsistent — and there's no order record yet at that
  point, because the insert happens last.
- **Silent correctness bug:** if `items` is empty, `total` is `0`, and the code
  happily calls Stripe to charge $0 and creates an order. Nothing validates that
  there's actually something being purchased.
- **Mixed error handling styles** — some paths return `400`, one returns `402`,
  and there's no catch around the DB writes at all, so a DB failure after a
  successful charge surfaces as an unhandled promise rejection.

## After

```javascript
// services/pricingService.js
function applyCoupon(total, coupon) {
  if (!coupon || coupon.expiresAt <= new Date()) return total;
  const discounted = coupon.type === 'percent'
    ? total - (total * coupon.value / 100)
    : total - coupon.value;
  return Math.max(discounted, 0);
}

module.exports = { applyCoupon };
```

```javascript
// services/checkoutService.js
const { applyCoupon } = require('./pricingService');

class CheckoutError extends Error {
  constructor(message, statusCode) {
    super(message);
    this.statusCode = statusCode;
  }
}

async function priceOrder({ items, couponCode }, { productRepo, couponRepo }) {
  if (!items || items.length === 0) {
    throw new CheckoutError('Cart is empty', 400);
  }

  let total = 0;
  const validatedItems = [];
  for (const item of items) {
    const product = await productRepo.findById(item.productId);
    if (!product) throw new CheckoutError(`Invalid product: ${item.productId}`, 400);
    if (product.stock < item.quantity) throw new CheckoutError(`Out of stock: ${product.name}`, 400);
    total += product.price * item.quantity;
    validatedItems.push({ product, quantity: item.quantity });
  }

  if (couponCode) {
    const coupon = await couponRepo.findByCode(couponCode);
    total = applyCoupon(total, coupon);
  }

  return { total, validatedItems };
}

async function completeCheckout(input, deps) {
  const { userId, stripeToken } = input;
  const { paymentGateway, productRepo, orderRepo } = deps;

  const { total, validatedItems } = await priceOrder(input, deps);

  const charge = await paymentGateway.charge(total, stripeToken)
    .catch(() => { throw new CheckoutError('Payment failed', 402); });

  // Decrement stock and record the order as a single logical unit so a
  // partial failure doesn't leave a charged customer with no order record.
  try {
    for (const { product, quantity } of validatedItems) {
      await productRepo.decrementStock(product._id, quantity);
    }
    return await orderRepo.create({ userId, items: validatedItems, total, chargeId: charge.id });
  } catch (err) {
    await paymentGateway.refund(charge.id);
    throw new CheckoutError('Order could not be completed; payment refunded', 500);
  }
}

module.exports = { priceOrder, completeCheckout, CheckoutError };
```

```javascript
// routes/checkout.js
const express = require('express');
const router = express.Router();
const { completeCheckout, CheckoutError } = require('../services/checkoutService');
const deps = require('../deps'); // wires real repos/paymentGateway from config

router.post('/checkout', async (req, res) => {
  try {
    const order = await completeCheckout(req.body, deps);
    res.json({ success: true, total: order.total });
  } catch (err) {
    if (err instanceof CheckoutError) {
      return res.status(err.statusCode).json({ error: err.message });
    }
    res.status(500).json({ error: 'Unexpected error' });
  }
});

module.exports = router;
```

```javascript
// services/__tests__/checkoutService.test.js
const { priceOrder, CheckoutError } = require('../checkoutService');

function fakeProductRepo(products) {
  return { findById: (id) => Promise.resolve(products.find(p => p._id === id) || null) };
}
function fakeCouponRepo(coupons) {
  return { findByCode: (code) => Promise.resolve(coupons.find(c => c.code === code) || null) };
}

test('prices a simple order with no coupon', async () => {
  const productRepo = fakeProductRepo([{ _id: 'p1', price: 20, stock: 5, name: 'Widget' }]);
  const { total } = await priceOrder(
    { items: [{ productId: 'p1', quantity: 2 }] },
    { productRepo, couponRepo: fakeCouponRepo([]) }
  );
  expect(total).toBe(40);
});

test('applies a percent coupon', async () => {
  const productRepo = fakeProductRepo([{ _id: 'p1', price: 50, stock: 5, name: 'Widget' }]);
  const couponRepo = fakeCouponRepo([{ code: 'SAVE20', type: 'percent', value: 20, expiresAt: new Date(Date.now() + 86400000) }]);
  const { total } = await priceOrder(
    { items: [{ productId: 'p1', quantity: 1 }], couponCode: 'SAVE20' },
    { productRepo, couponRepo }
  );
  expect(total).toBe(40);
});

test('rejects an empty cart instead of pricing it as $0', async () => {
  await expect(priceOrder({ items: [] }, { productRepo: fakeProductRepo([]), couponRepo: fakeCouponRepo([]) }))
    .rejects.toBeInstanceOf(CheckoutError);
});

test('rejects insufficient stock', async () => {
  const productRepo = fakeProductRepo([{ _id: 'p1', price: 10, stock: 1, name: 'Widget' }]);
  await expect(priceOrder({ items: [{ productId: 'p1', quantity: 5 }] }, { productRepo, couponRepo: fakeCouponRepo([]) }))
    .rejects.toBeInstanceOf(CheckoutError);
});
```

## What actually improved

- **Testability:** `priceOrder` is now a pure-ish function taking plain data and
  repo interfaces. The four tests above run in milliseconds with no HTTP server,
  no real database, and no real Stripe account — that's what "unit-testable"
  concretely buys you.
- **The empty-cart bug is now impossible to reintroduce silently** — it's an
  explicit `CheckoutError`, and there's a test asserting it.
- **Failure ordering is fixed:** stock is decremented and the order is recorded
  only after a successful charge, and if that step fails, the charge is refunded
  instead of leaving the customer billed with no order. This wasn't handled at
  all before.
- **The secret is gone from this file** — `paymentGateway` is injected via
  `deps.js`, which reads from environment variables (tying back to Issue 1 in the
  assessment).
- **The route handler is now ~10 lines** and does exactly one thing: translate
  HTTP in, call the service, translate the result back to HTTP. Someone reading
  `routes/checkout.js` no longer needs to understand coupon math to know what the
  endpoint does.
- **What I deliberately didn't do:** wrap everything in a database transaction.
  MongoDB transactions require a replica set and add real operational complexity;
  the refund-on-failure approach gets most of the safety with far less
  infrastructure change, and is a better fit for "ships incrementally without
  requiring an infra migration" than reaching for the most theoretically correct
  solution on day one.
