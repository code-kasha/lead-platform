# CLAUDE.md

Guidance for Claude Code when working in this repository.

## Project

Full-stack Lead Management Platform: Django REST Framework API + React/TypeScript SPA.
Covers authentication, lead capture, assignment, a validated status lifecycle, notes, and
an automatic activity timeline.

Repo: `github.com/code-kasha/lead-platform` · Author: Akash Damle

## Layout

```
backend/
  apps/
    accounts/   auth, custom user, role permissions
    common/     shared models, pagination, serializers, utils
    leads/      leads, notes, activities
  config/
    settings/   split settings, selected at runtime by DJANGO_ENV
frontend/
  src/
    api/        axios client + OpenAPI-generated types
    components/ reusable UI + layout
    layouts/    page shells
    pages/      route-level views
    routes/     routing and guards
docs/           architecture and written assessments
screenshots/    UI captures referenced by the README
```

## Architecture rules

- **Business logic belongs in `services.py`**, not in views. Views handle request/response
  only: `Request → View → Serializer → Service → Database`.
- **Service functions are transactional** and are the only place that writes activity records.
- **Status transitions are validated** in the leads service/validators — do not let a view
  mutate `status` directly.
- **API-first.** The backend owns the contract via drf-spectacular; the frontend consumes
  TypeScript types generated from `backend/schema.yml`. Do not hand-write API interfaces in
  the frontend — regenerate with `openapi-typescript`.
- Serializers for `leads` are split by concern under `apps/leads/serializers/`.

## Settings

`backend/config/settings/__init__.py` reads `DJANGO_ENV` and imports `production.py` when it
is `production`, otherwise `development.py`. `manage.py` sets `DJANGO_SETTINGS_MODULE` to the
package `config.settings` — not a specific module. Environment is read via `python-decouple`
from `.env`; `.env.example` lists the expected keys.

## Commands

```bash
# backend (from backend/)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
pytest

# frontend (from frontend/)
pnpm install
pnpm dev         # http://localhost:5173
pnpm lint
pnpm test        # vitest run (jsdom); `pnpm test:watch` to iterate
pnpm build       # tsc -b && vite build
```

Swagger is served at `/api/docs/` once the backend is running.

CI (`.github/workflows/ci.yml`) runs on PRs and pushes to `main`: flake8, a missing-migrations
check, a stale-schema check (`backend/schema.yml` must match `manage.py spectacular`), pytest,
a stale-types check (`frontend/src/types/api.ts` must match `openapi-typescript` output), then
`pnpm lint`, `pnpm test` and `pnpm build`. After changing views or serializers, regenerate both files:
`python manage.py spectacular --file schema.yml` (from `backend/`) and
`pnpm exec openapi-typescript ../backend/schema.yml -o src/types/api.ts` (from `frontend/`).
Python lint config is `.flake8` (max line length 120).

## Conventions

- Frontend source is **tab-indented**; match the surrounding file.
- Backend modules carry `# ===` banner comments above declarations — follow the local style.
- `frontend/src/api/axios.ts` builds its client from `VITE_API_URL` (e.g.
  `http://127.0.0.1:8000/api`). There is no dev proxy; `vite.config.ts` sets `envDir: ".."` so
  Vite reads the single repo-root `.env` (only `VITE_`-prefixed keys reach the client).
- Auth flow: `routes/RequireAuth.tsx` guards app routes (redirects to `/login` with the
  requested path in `state.from`). On a 401, `api/axios.ts` refreshes once (shared across
  concurrent requests, since refresh tokens rotate and the old one is blacklisted), retries,
  and calls `utils/session.ts#endSession` if the refresh fails. Use `clearTokens()` rather
  than touching `localStorage` keys directly.
- Frontend tests live next to the code as `*.test.ts(x)` (Vitest + Testing Library, jsdom).
  `src/test/setup.ts` clears `localStorage` and mocks between tests, and Vitest pins
  `VITE_API_URL` to a dummy host; stub requests with `vi.spyOn(api, ...)` or an axios adapter.
  Helpers in `src/test/`: `renderRoute` (query client + memory router), `fixtures.ts`, and
  `fakeLeadApi` (a stateful stand-in for one lead's endpoints that enforces the backend's
  status transitions).
- TanStack Query keys for a lead use the **numeric** id (`["lead", Number(id)]`); route params
  are strings, and `["lead", "7"]` would never match the `["lead", 7]` keys that mutations
  invalidate.

## Constraints

- **No third-party branding anywhere.** This repo was deliberately scrubbed of all references
  to a former client/company name, across the working tree, the screenshots, and the entire
  git history (which was rewritten, and the GitHub repo recreated, to remove it). Do not
  reintroduce client names, "built for X" credits, or branded deployment hostnames in code,
  docs, screenshots, commit messages, or repo metadata.
- Do not commit `.env`. It is untracked and holds live credentials.

## Known issues

- The backend requires **Python ≥ 3.12** (Django 6.0). Tests need `SECRET_KEY` and
  `DATABASE_URL` set (e.g. `DATABASE_URL=sqlite:///:memory:`); the full suite is 71 tests.
