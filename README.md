# Lead Management Platform

A production-ready **Lead Management Platform** built with **Django REST Framework** and **React**.

The platform enables sales teams to capture, manage, assign, and track leads throughout the sales pipeline. It features JWT authentication, role-based access control, lead assignment, workflow management, activity tracking, comprehensive OpenAPI documentation, and a layered architecture following Django and DRF best practices.

This project is being developed as part of the **Full Stack Development Assessment**.

---

# Features

## Authentication

- JWT Authentication
- Login
- Logout
- Token Refresh
- Current User endpoint
- Password hashing
- Protected REST API
- Role-based authorization

---

## Lead Management

- Create, retrieve, update and delete leads
- Lead assignment
- Lead status workflow
- Lead notes
- Lead activity history
- Server-side validation
- Business rule enforcement
- Automatic activity logging

---

## Search & Filtering

- Pagination
- Search by:
  - First name
  - Last name
  - Email
  - Phone
  - Company

- Filter by:
  - Status
  - Source
  - Creator
  - Assigned member

- Ordering support

---

## Notes

- Add notes
- Update notes
- Delete notes
- List notes for a lead

---

## Activity Tracking

- Automatic activity logging
- Assignment history
- Status change history
- Note activity
- Activity timeline endpoint

---

## API

- RESTful API
- OpenAPI 3 Specification
- Swagger UI
- ReDoc
- Standardised API responses
- Fully documented endpoints

---

## Architecture

- Modular Django application structure
- Service layer for business logic
- Serializer separation (Create / Update / Read)
- Custom permission classes
- PostgreSQL database
- Environment-based configuration
- Shared documentation components
- Typed codebase

---

# Technology Stack

## Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- drf-spectacular

## Frontend

- React
- Vite
- Axios
- React Router

---

# Project Structure

```text
backend/
├── config/
├── apps/
│   ├── accounts/
│   ├── common/
│   └── leads/
│       ├── serializers/
│       ├── services.py
│       ├── permissions.py
│       ├── filters.py
│       ├── docs.py
│       ├── tests/
│       └── views/
└── manage.py

frontend/
```

---

# API Documentation

Once the backend is running:

| Service        | URL            |
| -------------- | -------------- |
| Swagger UI     | `/api/docs/`   |
| ReDoc          | `/api/redoc/`  |
| OpenAPI Schema | `/api/schema/` |

---

# Authentication

All protected endpoints require a JWT access token.

```http
Authorization: Bearer <access_token>
```

Authentication endpoints

```http
POST /api/auth/login/
POST /api/auth/refresh/
POST /api/auth/logout/
GET  /api/auth/me/
```

---

# Main API Endpoints

## Leads

```http
GET    /api/leads/
POST   /api/leads/
GET    /api/leads/{id}/
PUT    /api/leads/{id}/
PATCH  /api/leads/{id}/
DELETE /api/leads/{id}/
```

## Business Operations

```http
POST /api/leads/{id}/assign/
POST /api/leads/{id}/status/
```

## Notes

```http
POST   /api/leads/{id}/notes/
GET    /api/leads/{id}/notes/list/
PATCH  /api/leads/notes/{id}/
DELETE /api/leads/notes/{id}/
```

## Activities

```http
GET /api/leads/{id}/activities/
```

---

# User Roles

## Administrator

- Full system access
- Manage all leads
- Assign leads
- Change lead status
- Manage notes
- View all activities

## Member

- View assigned and created leads
- Update assigned and created leads
- Change lead status
- Create notes
- Edit and delete own notes
- View lead activities

---

# Running Locally

## Clone the repository

```bash
git clone <repository-url>
cd lead-management-platform
```

## Create a virtual environment

```bash
python -m venv .venv
```

## Activate the environment

### Windows

```powershell
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Configure environment variables

Create a `.env` file.

```env
SECRET_KEY=
DEBUG=True

DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
```

## Apply migrations

```bash
python manage.py migrate
```

## Create a superuser

```bash
python manage.py createsuperuser
```

## Run the development server

```bash
python manage.py runserver
```

---

# Testing

Run the complete test suite

```bash
python manage.py test
```

Run tests for individual apps

```bash
python manage.py test apps.accounts
python manage.py test apps.leads
```

Generate the OpenAPI schema

```bash
python manage.py spectacular --file schema.yml
```

Run Django system checks

```bash
python manage.py check
```

---

# Project Status

## Completed

- Project setup
- JWT Authentication
- Custom User model
- Lead CRUD
- Lead assignment
- Lead status workflow
- Notes API
- Activity API
- Search & filtering
- Pagination
- Custom permissions
- Business service layer
- Swagger documentation
- ReDoc
- OpenAPI schema generation
- Comprehensive backend test suite

---

# Roadmap

- React frontend
- Dashboard
- Lead analytics
- Email notifications
- CSV export
- Docker support
- GitHub Actions
- CI/CD pipeline
- Redis caching
- Background tasks

---

# License

This project is licensed under the MIT License.
