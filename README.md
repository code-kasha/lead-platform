# Lead Management Platform

A production-ready Lead Management Platform built with Django REST Framework.

This application allows sales teams to capture, manage, assign, and track leads through a complete sales pipeline with secure authentication, role-based access control, activity tracking, and a RESTful API.

This project is being built as part of the **Full Stack Development Assessment**.

---

## Features

### Public Lead Capture

- Public lead submission form
- Spam protection (optional)
- Server-side validation
- Duplicate lead detection (optional)

### Authentication

- JWT Authentication
- Login / Logout
- Refresh Tokens
- Password hashing
- Protected API

### Roles

There are two application roles.

#### Admin

- View all leads
- Create/Edit/Delete leads
- Assign leads to members
- Change lead status
- Manage users
- View activity logs
- Add notes

#### Member

- View assigned leads
- Update assigned leads
- Add notes
- Change lead status (limited)
- View activity history

Permissions are enforced on both:

- Backend
- Frontend

---

## Lead Lifecycle

Example pipeline

```
New
↓

Contacted
↓

Qualified
↓

Proposal Sent
↓

Won
```

Alternative outcome

```
New
↓

Contacted
↓

Lost
```

Each status change is recorded in the activity history.

---

## Lead Information

Each lead contains:

- Name
- Email
- Phone
- Company
- Source
- Status
- Assigned User
- Created By
- Created Date
- Updated Date

---

## Notes

Every lead supports multiple notes.

Each note contains

- Author
- Timestamp
- Content

Notes cannot be edited after creation (optional business rule).

---

## Activity Trail

Every important action creates an activity entry.

Examples:

- Lead created
- Lead assigned
- Status changed
- Note added
- Lead updated

Activity entries contain

- User
- Action
- Timestamp
- Metadata

---

# Technology Stack

## Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- drf-spectacular (API docs)

## Frontend

- React
- Vite
- Axios
- React Router

## Deployment

Backend

- Render / Railway

Frontend

- Vercel / Netlify

Database

- PostgreSQL

---

# Project Structure

```
backend/
    config/
    apps/
        accounts/
        leads/
        notes/
        activities/

frontend/
```

---

# Database Design

## User

```
id
name
email
password
role
created_at
```

---

## Lead

```
id
name
email
phone
company
status
assigned_to
created_by
created_at
updated_at
```

---

## LeadNote

```
id
lead
author
note
created_at
```

---

## ActivityLog

```
id
lead
user
action
metadata
created_at
```

---

# API

## Authentication

```
POST /api/auth/login/

POST /api/auth/refresh/

POST /api/auth/logout/
```

---

## Leads

### List Leads

```
GET /api/leads/
```

Supports

- Pagination
- Search
- Filtering
- Ordering

Example

```
GET /api/leads/?status=new&page=2&page_size=20
```

---

### Create Lead

```
POST /api/leads/
```

---

### Retrieve Lead

```
GET /api/leads/{id}/
```

---

### Update Lead

```
PUT /api/leads/{id}/
PATCH /api/leads/{id}/
```

---

### Delete Lead

```
DELETE /api/leads/{id}/
```

(Admin only)

---

### Assign Lead

```
POST /api/leads/{id}/assign/
```

---

### Change Status

```
POST /api/leads/{id}/status/
```

---

### Notes

```
GET /api/leads/{id}/notes/

POST /api/leads/{id}/notes/
```

---

### Activity

```
GET /api/leads/{id}/activity/
```

---

# Status Codes

| Code | Meaning          |
| ---- | ---------------- |
| 200  | Success          |
| 201  | Created          |
| 204  | Deleted          |
| 400  | Validation Error |
| 401  | Unauthorized     |
| 403  | Forbidden        |
| 404  | Not Found        |
| 500  | Server Error     |

---

# Authentication

JWT Bearer Token

Example

```
Authorization: Bearer <access_token>
```

---

# Testing

Tests include

- Authentication
- Permissions
- CRUD
- Lead assignment
- Status changes
- Notes
- API validation

Run

```
python manage.py test
```

---

# Local Installation

Clone

```
git clone <repo>
```

Create virtual environment

```
python -m venv .venv
```

Activate

Windows

```
.venv\Scripts\activate
```

Linux

```
source .venv/bin/activate
```

Install dependencies

```
pip install -r requirements.txt
```

Environment variables

```
SECRET_KEY=

DEBUG=True

DATABASE_URL=

ALLOWED_HOSTS=

JWT_SECRET=
```

Run migrations

```
python manage.py migrate
```

Create admin

```
python manage.py createsuperuser
```

Run server

```
python manage.py runserver
```

---

# Deployment

Backend

Render

Frontend

Vercel

Database

PostgreSQL

---

# Demo Credentials

Admin

```
email:
password:
```

Member

```
email:
password:
```

---

# Live Demo

Frontend

```
Coming Soon
```

Backend

```
Coming Soon
```

---

# Footer Requirement

Every page includes the footer

> Built for Training Task

linked to

https://example.com

---

# License

MIT
