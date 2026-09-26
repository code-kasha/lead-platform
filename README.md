# Lead Management Platform

A full-stack lead management application built with Django REST Framework and React. It demonstrates a service-oriented backend architecture, role-based access control, an API-first contract with generated TypeScript types, and a modern React dashboard for managing sales leads.

---

## Overview

The application covers the complete lead workflow: authentication, lead capture, assignment, lifecycle tracking, notes, and an automatic activity history.

Development follows an API-first approach — the backend publishes an OpenAPI specification, and the frontend consumes TypeScript models generated from it rather than maintaining duplicate interfaces by hand.

---

## Features

### Authentication

- JWT authentication with token refresh
- Secure logout (token blacklisting)
- Current-user endpoint
- Role-based access control

### Lead Management

- Create, view, update, and delete leads
- Lead assignment to users
- Status lifecycle with transition validation
- Search, filtering, and ordering

### Collaboration

- Notes with create / edit / delete
- Automatic activity timeline
- Assignment and status-change history

### API

- RESTful endpoints with consistent response serializers
- OpenAPI / Swagger documentation
- Type-safe contracts shared with the frontend

### Frontend

- Responsive dashboard with protected routes
- React Query for server state
- Reusable UI component set
- Toast notifications and loading/empty/error states
- TypeScript models generated from OpenAPI

---

## Technology Stack

**Backend** — Python, Django, Django REST Framework, Simple JWT, drf-spectacular, django-filter, PostgreSQL

**Frontend** — React, TypeScript, Vite, React Query, React Router, Axios, Tailwind CSS, React Hook Form, Zod, React Hot Toast

---

## Project Structure

```
backend/
  apps/
    accounts/      authentication, users, permissions
    common/        shared models, pagination, serializers, utils
    leads/         leads, notes, activities
      services/    business logic
      serializers/ request & response shapes
      filters/     query filtering
  config/
    settings/      split settings (base / development / production)

frontend/
  src/
    api/           axios client + generated OpenAPI types
    components/    reusable UI and layout
    layouts/       page shells
    pages/         route-level views
    routes/        routing and route guards
    types/         shared types
```

Business logic lives in dedicated service functions; views stay responsible only for request handling.

```
Request → View → Serializer → Service → Database
```

---

## Business Rules

Leads move through a configurable lifecycle:

```
NEW → CONTACTED → QUALIFIED → PROPOSAL → WON
```

A lead may also transition to **LOST** from any intermediate stage where permitted. Invalid transitions are rejected at the service layer, and every significant action writes an activity record automatically.

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+ and pnpm
- PostgreSQL (or set `DATABASE_URL` to a hosted instance)

### Environment

Copy the example file and fill in your own values:

```bash
cp .env.example .env
```

| Variable | Description |
| --- | --- |
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for local development |
| `DJANGO_ENV` | `development` or `production` |
| `ALLOWED_HOSTS` | Comma-separated host list |
| `DATABASE_*` / `DATABASE_URL` | Database connection settings |
| `VITE_API_URL` | Base URL of the API, e.g. `http://127.0.0.1:8000/api` |

### Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Frontend

```bash
cd frontend
pnpm install
pnpm dev
```

The frontend runs on `http://localhost:5173` and expects the API at `VITE_API_URL`.

---

## API Documentation

With the backend running, Swagger UI is available at:

```
/api/docs/
```

The OpenAPI schema is committed at `backend/schema.yml`. Frontend types are regenerated from it with `openapi-typescript`.

---

## Testing & Quality

```bash
# backend
cd backend && pytest

# frontend
cd frontend && pnpm lint && pnpm build
```

---

## Screenshots

Application screenshots are in [`screenshots/`](screenshots/).

---

## Documentation

Additional design notes live in [`docs/`](docs/), including `ARCHITECTURE.md` and a set of assessment, migration, refactor, and standards write-ups.

---

## Future Improvements

- Email notifications
- Dashboard analytics
- File attachments
- Lead reminders
- Advanced reporting
- Bulk lead operations

---

## Author

Akash Damle
