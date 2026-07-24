# Architecture & Planning

## Project

**Lead Management Platform**

A Lead Management application built using **Django**, **Django REST Framework**, and **PostgreSQL**.

This document summarizes the initial architecture and database design completed during **Phase 1 - Planning**.

---

# Phase 1 Status

**Status:** ✅ Complete

Completed tasks:

- Requirements analysis
- Technology selection
- Application architecture
- Database design
- Entity relationship design
- Initial project structure
- Business entity identification

---

# Technology Stack

## Backend

- Python 3.13+
- Django
- Django REST Framework
- PostgreSQL

## Authentication

- JWT Authentication
- Custom User Model

## API Documentation

- drf-spectacular (OpenAPI / Swagger)

## Frontend

- React
- Vite
- React Router
- Axios

## Deployment

Backend

- Render / Railway

Frontend

- Vercel / Netlify

Database

- PostgreSQL

---

# Architecture

The application follows a layered architecture to separate concerns.

```
Client

↓

API (Views / ViewSets)

↓

Serializers

↓

Services (Business Logic)

↓

Models

↓

PostgreSQL
```

Business logic should reside in **service classes**, keeping views and serializers lightweight and focused on request handling and validation.

---

# Django Apps

```
apps/

    accounts/

    leads/

    activities/

    common/
```

## accounts

Responsible for:

- Authentication
- User model
- Permissions

## leads

Responsible for:

- Lead management
- Lead notes
- Business logic
- REST API

## activities

Responsible for:

- Audit trail
- Activity logging

## common

Responsible for:

- BaseModel
- Pagination
- Shared utilities
- Constants
- Custom permissions

---

# Database Design

## User

Stores application users.

Fields

- id
- email
- password
- first_name
- last_name
- role
- is_active
- is_staff
- created_at
- updated_at

Roles

- ADMIN
- MEMBER

---

## Lead

Stores customer leads.

Fields

- id
- name
- email
- phone
- company
- source
- status
- assigned_to
- created_by
- created_at
- updated_at

Status Pipeline

```
NEW

↓

CONTACTED

↓

QUALIFIED

↓

PROPOSAL_SENT

↓

WON
```

Alternative ending

```
NEW

↓

CONTACTED

↓

LOST
```

Lead Sources

- Website
- Facebook
- Instagram
- Referral
- Manual
- Other

---

## LeadNote

Stores notes associated with a lead.

Fields

- id
- lead
- author
- note
- created_at

A lead may contain multiple notes.

---

## ActivityLog

Stores an immutable audit trail.

Fields

- id
- lead
- user
- action
- field_name
- old_value
- new_value
- metadata
- created_at

Supported actions

- LEAD_CREATED
- LEAD_UPDATED
- LEAD_ASSIGNED
- STATUS_CHANGED
- NOTE_ADDED
- LEAD_DELETED

---

# Entity Relationships

- One User can create many Leads.
- One User can be assigned many Leads.
- One Lead can contain many Notes.
- One User can create many Notes.
- One Lead can contain many Activity Logs.
- One User can perform many Activities.

---

# ER Diagram

```
                        +----------------------+
                        |       User           |
                        +----------------------+
                        | PK id               |
                        | email              |
                        | password           |
                        | first_name         |
                        | last_name          |
                        | role              |
                        +----------------------+
                          ▲             ▲
                          │             │
               created_by │             │ assigned_to
                          │             │
                 +-----------------------------+
                 |            Lead             |
                 +-----------------------------+
                 | PK id                      |
                 | name                       |
                 | email                      |
                 | phone                      |
                 | company                    |
                 | source                     |
                 | status                     |
                 | created_at                 |
                 | updated_at                 |
                 +-----------------------------+
                     ▲                    ▲
                     │                    │
                     │                    │
          +----------------+      +----------------------+
          |   LeadNote     |      |    ActivityLog       |
          +----------------+      +----------------------+
          | PK id          |      | PK id               |
          | FK lead        |      | FK lead             |
          | FK author      |      | FK user             |
          | note           |      | action              |
          | created_at     |      | field_name          |
          +----------------+      | old_value           |
                                  | new_value           |
                                  | metadata            |
                                  | created_at          |
                                  +----------------------+
```

---

# Design Decisions

## Custom User Model

A custom User model will be implemented from the start to avoid future migration issues and allow role-based authorization.

---

## Role-Based Authorization

Two roles will be supported:

- Admin
- Member

Permissions will be enforced at both the API and frontend levels.

---

## Lead Status

Lead status will use Django `TextChoices` instead of free-text values to ensure consistency and simplify validation.

---

## Activity Logging

An immutable activity log will record all significant changes, including creation, assignment, status changes, note additions, updates, and deletion.

---

## Notes

Lead notes are append-only records with timestamps, preserving a complete history of interactions.

---

## Shared BaseModel

All models will inherit from a common abstract `BaseModel` that provides `created_at` and `updated_at` timestamps to ensure consistency and reduce duplication.

---

# Future Enhancements

The following features are outside the current assignment scope but are planned as possible enhancements:

- Lead tags
- Email notifications
- File attachments
- CSV export
- Dashboard analytics
- Redis caching
- Celery background tasks
- Docker support
- GitHub Actions CI/CD
- Soft delete
- Audit reporting

---

# Phase 1 Summary

Phase 1 established the application's architecture and data model before implementation.

The project now has:

- A defined technology stack
- Layered architecture
- Normalized database schema
- Entity relationship diagram
- Business rules
- Project structure
- Foundation for API development

**Phase 1 Status:** ✅ Complete

The next phase is **Phase 2 – Backend Setup**, where the Django project, applications, and development environment will be initialized.
