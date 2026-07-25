# Task B — Phased Migration Plan

No big-bang rewrite. The service processes live orders and can't go down, which
rules out a parallel "v2" rebuild — that approach only works if you can afford to
run two systems and cut over, and a small team supporting live payments usually
can't. Instead, this plan improves the system in place, one vertical slice at a
time, so it's always shippable and rollback is always just "revert the last PR."

## Week 1 — Stop the bleeding

Goal: eliminate active security exposure. Nothing here touches business logic, so
risk of regression is low and it can ship fast.

- Rotate all committed credentials (payment gateway keys, DB connection string,
  any third-party API keys found in `config.js` or elsewhere in the repo).
- Move all secrets to environment variables via the hosting platform's secret
  manager; confirm `.env` is gitignored.
- Add secret-scanning to CI (gitleaks or equivalent) so this regresses loudly, not
  silently.
- Build minimal read-only API endpoints for the handful of screens currently
  hitting MongoDB directly from the frontend; point those screens at the new
  endpoints; remove the client-side DB connection entirely.
- **Ship criteria:** no credentials in the repo, no client-side DB access,
  CI scanning in place. This is a deploy-and-verify week, not a big-PR week.

## Month 1 — Make the checkout path safe to change

Goal: the highest-risk, most-changed part of the system (checkout, pricing,
inventory, refunds) gets a service layer and a real test suite, so future work on
it stops being a gamble.

- Write golden-path integration tests for checkout and refund *against the
  current, unrefactored code* first. These tests describe current behavior and
  become the safety net for the refactor that follows — this order matters, since
  refactoring before you have tests means you have no way to prove you didn't
  break anything.
- Extract `checkoutService`, `pricingService`, and `inventoryService` out of the
  route handlers, one at a time, each behind the integration tests plus new unit
  tests for the extracted module. (See `refactor-before-after.md` for what one of
  these extractions looks like concretely.)
- Each extraction ships as its own small PR and deploy — not one giant "refactor
  checkout" PR. Small, reviewable, revertible.
- Set up basic CI: lint + test on every PR, blocking merge on failure. This
  doesn't exist yet and is a prerequisite for trusting the tests going forward.
- **Ship criteria:** checkout and refund logic is unit-testable and covered;
  route handlers are thin (parse request → call service → format response); CI
  runs tests on every PR.

## Quarter 1 — Extend the pattern, retire the debt

Goal: apply the same service-layer + test pattern to the rest of the app, and
close out the remaining structural debt that wasn't urgent enough for week 1 or
month 1.

- Extract remaining business logic (order history, customer notifications,
  admin reporting) into services following the same pattern, in order of how
  often each area currently gets touched — the parts changing most often get the
  safety net soonest, same prioritization logic as the checkout work.
- Scrub secrets from git history (BFG or `git-filter-repo`) now that rotation has
  already neutralized the immediate exposure — this was explicitly deferred out
  of week 1 because rotation, not history-scrubbing, is what stops the leak from
  being exploitable.
- Introduce a lightweight architecture doc (even one page) describing the
  route → service → data-access layering, so new contributors don't reintroduce
  logic-in-handlers by default.
- Add monitoring/alerting on the checkout and refund paths specifically, since
  those are the flows this whole plan has been protecting.
- Revisit whether MongoDB's schema-less flexibility is still helping or now just
  hiding data-integrity bugs that a schema layer (e.g. Mongoose schemas with
  validation, or a migration to a relational store) would catch earlier. This is
  explicitly a "revisit," not a commitment — it needs its own risk/cost
  assessment once the more urgent items are done, not a decision made under this
  plan's time pressure.

## Why this ordering and not another

Security exposure comes before code quality because the cost of delay is
categorically different — a leaked credential can cause an incident *today*;
tangled route handlers make future work slower but aren't actively harming
anyone right now. Tests come *with* the refactor, not before it in isolation and
not after it as cleanup, because tests-in-isolation end up testing the wrong
thing (the tangle) and tests-after-the-fact don't protect the refactor that
needed protecting. Everything ships as small, revertible increments because
"cannot go down" means every change needs a fast, low-drama rollback path, and
that's much easier to guarantee for a 200-line PR than a 4,000-line one.
