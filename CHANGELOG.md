# Changelog

## 1.0.0 (2026-09-26)

The first and final planned release. lead-platform is complete as of this version and not actively maintained; fork it freely.

- **Leads API:** create, list, retrieve, edit and delete leads. Filter by status, assignee, creator and company; search across name, email, phone and company; sort; and paginate (20 per page, up to 100). OpenAPI 3 docs are at `/api/docs/` and `/api/redoc/`.
- **Status pipeline:** New → Contacted → Qualified → Proposal → Won, and Lost from any open stage. Transitions are enforced by one service function, and a blocked change returns `400` with the reason.
- **Activity timeline:** creating, editing, status changes, assignment and notes are recorded automatically, in the same transaction as the change.
- **Roles:** Admins see and manage every lead; Members see and work on the leads they created or are assigned to. Only Admins delete or assign. Notes are edited or deleted by their author or an Admin. A lead a member can't see returns `404`.
- **Authentication:** JWTs with 15-minute access tokens and 7-day refresh tokens that rotate and are blacklisted after use. Includes logout, the current user, and the list of assignable members.
- **Public lead form:** an unauthenticated endpoint for a website enquiry form, rate-limited per client (`PUBLIC_LEADS_RATE`, default 20 an hour).
- **Web app:** React 19 and TypeScript, with types generated from the API schema. Sign-in with a shared, single-flight token refresh; a dashboard; a searchable, filterable and paginated lead list; and a lead page with status, assignment, notes and the timeline.
- **Quality:** 99 backend tests and 74 frontend tests. CI runs flake8, a missing-migrations check, a stale-schema and stale-types check, ESLint, a production build, and a Docker build with a smoke test.
- **Deployment:** one Docker image (amd64 and arm64) serves the API, Django admin and the web app with gunicorn and WhiteNoise. It applies migrations and creates the first admin on start. There is a Render blueprint for a free demo on Neon Postgres, and a `docker compose` setup for local Postgres.

Release assets: `schema.yml` (the OpenAPI schema) and `SHA256SUMS`. Container image: `ghcr.io/code-kasha/lead-platform:v1.0.0` (also `latest`).
