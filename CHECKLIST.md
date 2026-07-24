# Lead Management Platform Checklist

---

# Phase 1 - Planning

- [x] Read assignment completely
- [x] Design database
- [x] Draw ER Diagram
- [x] Decide API endpoints
- [x] Create GitHub repository
- [x] Setup README

---

# Phase 2 - Backend Setup

- [x] Create Django project
- [x] Create virtual environment
- [x] Install Django
- [x] Install Django REST Framework
- [x] Install PostgreSQL driver
- [x] Install JWT package
- [x] Install drf-spectacular
- [x] Configure settings
- [x] Setup environment variables
- [x] Configure project structure
- [x] Configure development settings
- [x] Configure production settings
- [x] Configure logging

---

# Phase 3 - Authentication

- [x] Custom User model
- [x] User manager
- [x] Role field
- [x] JWT Login
- [x] JWT Refresh
- [x] JWT Logout
- [x] Current User endpoint
- [x] Password hashing
- [x] Authentication middleware
- [x] JWT blacklist
- [x] Permission classes

---

# Phase 4 - Models

## User

- [x] User model

## Lead

- [x] Lead model
- [x] Validation
- [x] Status choices
- [x] Assignment fields

## Notes

- [x] LeadNote model

## Activity

- [x] LeadActivity model

---

# Phase 5 - Lead CRUD API

## Authentication

- [x] Login
- [x] Refresh
- [x] Logout
- [x] Current user

## Leads

- [x] List
- [x] Create
- [x] Retrieve
- [x] Update
- [x] Delete

---

# Phase 6 - Query Features

- [ ] Pagination
- [ ] Search
- [ ] Filter by status
- [ ] Filter by source
- [ ] Filter by creator
- [ ] Filter by assigned user
- [ ] Ordering

---

# Phase 7 - Business APIs

## Assignment

- [ ] Assign endpoint

## Status

- [ ] Change status endpoint

## Notes

- [ ] Add note
- [ ] Edit note
- [ ] Delete note
- [ ] List notes

## Activity

- [ ] List activities

---

# Phase 8 - Permissions

- [ ] Admin permissions
- [ ] Member permissions
- [ ] Object-level permissions
- [ ] Test forbidden access

---

# Phase 9 - Business Logic

- [ ] Automatic activity logging
- [ ] Assignment validation
- [ ] Status transition rules
- [ ] Timestamp notes
- [ ] Duplicate lead detection
- [ ] Prevent self-assignment (optional)

---

# Phase 10 - Testing

## Accounts

- [x] Authentication tests
- [x] User model tests
- [x] Permission tests

## Leads

- [x] Model tests
- [x] Validator tests

## Remaining

- [ ] CRUD API tests
- [ ] Assignment tests
- [ ] Status tests
- [ ] Notes API tests
- [ ] Activity API tests
- [ ] Permission integration tests
- [ ] Filtering tests
- [ ] Search tests
- [ ] Pagination tests

---

# Phase 11 - Documentation

- [ ] README
- [x] Swagger UI
- [x] ReDoc
- [x] OpenAPI schema
- [x] Endpoint documentation
- [x] Response examples
- [ ] README API section
- [ ] Screenshots
- [ ] Demo credentials

---

# Phase 12 - Frontend

## Public

- [ ] Lead capture page

## Authentication

- [ ] Login

## Dashboard

- [ ] Dashboard layout
- [ ] Lead list
- [ ] Lead details
- [ ] Notes
- [ ] Activity timeline
- [ ] Status updates
- [ ] Assignment
- [ ] User management

---

# Phase 13 - Deployment

## Backend

- [ ] Deploy backend
- [ ] PostgreSQL
- [ ] Environment variables
- [ ] Static files
- [ ] HTTPS

## Frontend

- [ ] Deploy frontend

---

# Phase 14 - Assignment Deliverables

- [ ] Public GitHub repository
- [ ] Live backend
- [ ] Live frontend
- [ ] API documentation
- [ ] Admin credentials
- [ ] Member credentials
- [ ] Footer requirement
- [ ] Verify permissions
- [ ] Final testing

---

# Task B

## Assessment

- [ ] Architecture review
- [ ] Risk analysis
- [ ] Technical debt

## Migration Plan

- [ ] Week 1
- [ ] Month 1
- [ ] Quarter 1

## Refactoring

- [ ] Poor implementation
- [ ] Refactored implementation
- [ ] Improvement explanation

## Engineering Standards

- [ ] Code review policy
- [ ] Git workflow
- [ ] Branch strategy
- [ ] Testing strategy
- [ ] CI/CD proposal
- [ ] Coding standards
- [ ] Documentation standards

---

# Nice-to-have

- [ ] Email notifications
- [ ] CSV export
- [ ] Dashboard analytics
- [ ] Lead tags
- [ ] Soft delete
- [ ] Audit history
- [ ] Rate limiting
- [ ] Docker
- [ ] GitHub Actions
- [ ] Redis caching
- [ ] Celery
