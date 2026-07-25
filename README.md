# Lead Management Platform

A full-stack Lead Management Platform built with Django REST Framework and React. The project demonstrates a clean service-oriented backend architecture, role-based access control, typed API integration, and a modern React frontend for managing sales leads.

---

# Live Link : https://example.com

## NOTE: I am using free tier hosting, so the performance may be sub par. I strongly recommend local testing, Also this was made in a very short time and I have tried to elevate it as much as I could.

## Use of AI Tools

AI tools (Claude and ChatGPT) were used during development for `Scaffolding bolierplate, creating documents, I use AI and make it write tons of code, I select and refine thus making the product better`. All architectural decisions, the permission model, and the final code were reviewed and written/adjusted by me.

---

## Overview

The application provides a complete lead management workflow from authentication through lead creation, assignment, lifecycle tracking, notes, and activity history.

The project follows an API-first development approach using OpenAPI documentation and generated TypeScript models to ensure consistency between the backend and frontend.

---

## Features

### Authentication

- JWT Authentication
- Token Refresh
- Secure Logout
- Current User Endpoint
- Role Based Access Control

---

### Lead Management

- Create Leads
- View Lead Details
- Update Leads
- Delete Leads
- Lead Assignment
- Lead Status Workflow
- Search
- Filtering
- Ordering

---

### Lead Collaboration

- Add Notes
- Edit Notes
- Delete Notes
- Automatic Activity Timeline
- Assignment History
- Status Change History

---

### API

- RESTful API
- OpenAPI / Swagger Documentation
- Type-safe API contracts
- Consistent response serializers

---

### Frontend

- Responsive Dashboard
- Protected Routes
- React Query Server State
- Toast Notifications
- Reusable UI Components
- TypeScript
- Generated OpenAPI Types

---

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework
- Simple JWT
- drf-spectacular
- Django Filter

### Frontend

- React
- TypeScript
- Vite
- React Query
- React Router
- Axios
- Tailwind CSS
- React Hot Toast

---

## Project Architecture

### Backend

```
apps/

accounts/
common/
leads/

services/
serializers/
permissions/
filters/
docs/
```

Business logic is separated into dedicated service functions while views remain responsible only for request handling.

```
Request
    ↓

View
    ↓

Serializer
    ↓

Service
    ↓

Database
```

---

### Frontend

```
src/

api/
components/
layouts/
pages/
routes/
types/
```

The frontend consumes generated OpenAPI TypeScript models rather than maintaining duplicate interfaces manually.

---

## Business Rules

The application enforces configurable lead lifecycle rules.

```
NEW
    ↓
CONTACTED
    ↓
QUALIFIED
    ↓
PROPOSAL
    ↓
WON
```

A lead may also transition to **LOST** from any intermediate stage where permitted.

Every significant action automatically creates an activity record.

---

## Implementation Highlights

### Service-Oriented Backend

Business rules are encapsulated inside dedicated service functions rather than view classes.

### API-First Development

The backend exposes a documented OpenAPI specification consumed directly by the frontend.

### Type Safety

TypeScript models are generated from the OpenAPI schema, eliminating duplicated API contracts.

### Automatic Activity Logging

Assignments, status transitions and notes automatically create audit entries.

### Role-Based Permissions

Different operations are protected using custom permission classes.

### React Query

Server state is cached and automatically refreshed after mutations.

---

## Running the Project

### Backend

```bash
pip install -r requirements.txt

python manage.py migrate

python manage.py runserver
```

---

### Frontend

```bash
pnpm install

pnpm dev
```

---

## API Documentation

Swagger documentation is available after starting the backend.

```
/api/docs/
```

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
