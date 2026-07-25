# Task B — Assessment: Inheriting the Order Service

**Scenario used for this exercise:** a Node.js/Express + MongoDB "order service" that
handles checkout for a mid-sized e-commerce customer. It has been in production for
~18 months, has no tests, business logic lives inside route handlers, the React
frontend calls MongoDB directly for a handful of "quick" read screens, and API
keys/DB credentials are committed in `config.js`. It cannot go down — it processes
live orders and payment webhooks.

This document is my assessment: what I'd fix, in what order, and what it costs the
business if each issue is left alone.

## How I prioritized

I sorted issues by **(blast radius) × (probability of being triggered soon)**, not
by how ugly the code is. A codebase can be embarrassing and safe, or clean-looking
and one bad deploy away from leaking customer payment data. The second kind gets
fixed first regardless of effort.

## Issue 1 — Secrets committed to the repo
**Fix order: immediate, day 1, before anything else.**

This is the only issue on this list where doing nothing is not a viable choice for
even one more sprint. Live payment gateway keys and the DB connection string are in
git history, which means they're in every clone, every CI log, every laptop of
everyone who has ever had repo access — and rotating them later doesn't remove them
from history.

- **Risk of leaving it:** a leaked payment key is a direct financial and compliance
  exposure (PCI scope). A leaked DB credential is a direct path to a customer data
  breach. This is the one item where the downside is "front-page incident," not
  "annoying bug."
- **Fix:** rotate every credential currently in the repo (assume all of them are
  burned), move to environment variables loaded via the platform's secret manager,
  add `.env` to `.gitignore`, and add a pre-commit/CI secret-scanning check
  (e.g. gitleaks) so this can't silently happen again. Scrubbing git history
  (BFG/git-filter-repo) is a nice-to-have after rotation — rotation is what
  actually neutralizes the exposure, so it can't wait for a history rewrite.

## Issue 2 — Frontend calling the database directly
**Fix order: week 1, second priority.**

A handful of "quick" dashboard reads go straight from the React app to MongoDB
using a client-side DB library and a connection string shipped to the browser.

- **Risk of leaving it:** the DB connection string is exposed to anyone who opens
  dev tools, which means read access — and depending on how it's scoped, write
  access — to the production database is effectively public. This is a second,
  independent path to the same breach as Issue 1, and it's worse in one respect:
  it's baked into the shipped frontend bundle, not just git history.
- **Fix:** these screens need real API endpoints, even minimal read-only ones,
  behind the same auth middleware as the rest of the service. Given it's "a
  handful" of screens, this is a 1-2 day job, not a redesign — which is exactly
  why it goes in week 1 rather than being deferred into the bigger migration plan.

## Issue 3 — Business logic inside route handlers
**Fix order: ongoing, starting month 1, prioritized by which routes change most.**

Order pricing, discount stacking, inventory decrement, and refund logic all live
directly inside `app.post('/checkout', ...)` and similar handlers, mixed with
request parsing and response formatting.

- **Risk of leaving it:** this isn't a security risk, it's a *velocity and
  correctness* risk. Every new feature requires editing code that's also handling
  HTTP concerns, which means every change has more surface area for regressions,
  and nothing here is unit-testable without spinning up an HTTP server. The
  business risk compounds over time — the longer this is untouched, the more new
  logic gets bolted onto the same tangled handlers, and the more expensive
  eventual extraction becomes.
- **Fix:** extract into a service layer (`checkoutService`, `pricingService`,
  `inventoryService`) that route handlers call into. This is the subject of the
  concrete refactor in the companion document — I don't want to describe it twice,
  so see `refactor-before-after.md` for the actual before/after.
- **Why it's not #1 despite being the biggest chunk of work:** it's a correctness
  and maintainability problem, not an active-exposure problem. Nobody is
  currently being harmed by it the way they would be by leaked credentials. It's
  urgent, but it's not an emergency, and it needs to be done carefully — rushing
  a logic extraction on a payment path is how you cause the outage you're trying
  to avoid.

## Issue 4 — No automated tests
**Fix order: starts month 1, in lockstep with Issue 3, continues quarter 1.**

I'm deliberately not putting "write tests" as its own standalone top-line item.
Tests without a service layer to test are shallow (you end up writing brittle
end-to-end HTTP tests for everything, which is slow and doesn't pin down business
logic). Instead, every extraction in Issue 3 ships with tests for the logic being
extracted — that's what makes the extraction verifiably safe rather than a
guess.

- **Risk of leaving it:** every deploy is a gamble. Nobody can refactor anything
  else on this list with confidence, because there's no safety net to catch a
  regression. This is also why it can't be fixed with a single "add a test suite"
  sprint — a test suite bolted onto still-tangled route handlers only tests the
  tangle, not the logic.
- **Fix:** golden-path integration tests for checkout and refund first (the two
  flows that touch money), since they give the most safety per hour spent, then
  unit tests for each service module as it's extracted.

## Summary table

| Order | Issue | Type of risk | When |
|---|---|---|---|
| 1 | Secrets in repo | Active security/compliance exposure | Day 1 |
| 2 | Frontend → DB direct calls | Active security exposure | Week 1 |
| 3 | Logic in route handlers | Velocity/correctness, compounding | Month 1 → ongoing |
| 4 | No tests | Removes safety net for everything else | Month 1 → Quarter 1, paired with #3 |

The short version: fix what's actively exposed first, then fix what makes
everything else unsafe to touch, and don't try to do the big structural cleanup
in one pass — that's what the migration plan (next document) is for.
