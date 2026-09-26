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
requirements/   split dependency pins (base / auth / final)
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
pnpm build       # tsc -b && vite build
```

Swagger is served at `/api/docs/` once the backend is running.
Python lint config is `.flake8` (max line length 120).

## Conventions

- Frontend source is **tab-indented**; match the surrounding file.
- Backend modules carry `# ===` banner comments above declarations — follow the local style.
- `frontend/src/api/axios.ts` builds its client from `VITE_API_URL`. There is no dev proxy in
  `vite.config.ts`, so this variable must be set or every request resolves against the Vite
  origin and 404s.

## Constraints

- **No third-party branding anywhere.** This repo was deliberately scrubbed of all references
  to a former client/company name, across the working tree, the screenshots, and the entire
  git history (which was rewritten, and the GitHub repo recreated, to remove it). Do not
  reintroduce client names, "built for X" credits, or branded deployment hostnames in code,
  docs, screenshots, commit messages, or repo metadata.
- Do not commit `.env`. It is untracked and holds live credentials.

## Known issues

- `backend/pytest.ini` sets `DJANGO_SETTINGS_MODULE=config.settings.dev`, but no `dev.py`
  exists under `config/settings/` (the module is `development.py`, and the package itself
  resolves the environment). This looks like it would break collection; it was not verified
  here because pytest is not installed in the current interpreter. Confirm before trusting
  the "62 tests passing" claim in `CHECKLIST.md`.
- `VITE_API_URL` is currently empty in `.env`; set it before running the frontend.
- The GitHub repo description is blank after the repo was recreated.
