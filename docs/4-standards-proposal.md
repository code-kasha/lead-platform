# Task B — Standards Proposal

## The standards

Kept to a short list on purpose. A 40-item style guide nobody reads is worse than
five rules everyone actually follows. Each one exists because it directly
prevents one of the four issues in the assessment.

1. **No secrets in the repo, ever.** Enforced by CI secret-scanning
   (gitleaks), not just a wiki page. All config comes from environment
   variables; a `.env.example` documents what's needed without containing real
   values.

2. **Route/controller layer has no business logic.** Handlers parse the
   request, call a service function, and format the response — nothing else. If
   a handler has an `if` statement that isn't about HTTP status codes, that
   logic belongs in a service.

3. **Frontend talks to the API, never to the database.** No exceptions for
   "just one quick read screen" — that exception is exactly how the current
   problem started.

4. **New business logic ships with tests.** Not 100% coverage as a vanity
   metric — specifically, every new or touched service function gets a test for
   its main path and its main failure path. CI blocks merge if tests fail or if
   new service code has zero test coverage.

5. **Every PR is small enough to revert independently.** Roughly: if you can't
   describe what it does in one sentence, it's probably two PRs. This is what
   makes "cannot go down" survivable — rollback is a `git revert`, not an
   archaeology project.

## Why these five and not more

Each rule maps directly to one of the four issues in the assessment document.
That's deliberate — I didn't want to introduce a standards document that reads
like generic best-practice advice unconnected to what actually went wrong here.
A team that's never had a credentials leak doesn't need rule 1 emphasized the
same way; this team does, right now, because of what's in the repo today.

## Getting a resistant team to actually adopt these

The realistic failure mode for a standards doc isn't disagreement, it's quiet
non-compliance — everyone nods in the meeting and then the next PR looks exactly
like the old ones, because the old pattern is faster in the moment and nobody
wants to be the one person doing it "the new way" while everyone else doesn't.

- **Don't lead with the document.** Lead with the refactor. Showing one real,
  working before/after (like the checkout extraction) is worth more than any
  amount of "here's why we should do this" — it answers "does this actually work
  here, on our code" before anyone has to take it on faith.
- **Make the safe path the easy path.** If following the standard means more
  typing than not following it, people won't follow it under deadline pressure —
  that's not a discipline problem, it's a tooling problem. A service-layer
  template/generator, a lint rule that flags DB calls inside route files, and CI
  that blocks on missing tests all make the standard the path of least
  resistance rather than an extra step people have to remember.
- **Apply new standards to new/touched code only, not as a retroactive mandate.**
  Nobody needs to refactor code they're not currently working on just to satisfy
  a new rule. This keeps the ask proportional and avoids the "we'll never
  finish this" reaction that kills adoption of any big cleanup effort.
- **Bring the skeptics into the first extraction, not after it.** If someone's
  going to push back, pairing with them on the first real service extraction
  turns "why are we doing this" into "I helped build the pattern," which changes
  who defends it in code review six weeks later.
- **Make code review the enforcement mechanism, not a separate audit.** A
  checklist item in the PR template ("business logic in a service, not the
  handler? tests for the main path?") costs nothing extra and catches drift
  before merge, rather than in a quarterly retrospective when it's already
  compounded.
- **Revisit the list itself after a month.** If a rule is being routinely
  ignored, that's data — either it needs better tooling support or it wasn't
  the right rule. Standards that never get revised read as imposed-from-above
  rather than the team's own working agreement, which is exactly the dynamic
  that produces resistance in the first place.
