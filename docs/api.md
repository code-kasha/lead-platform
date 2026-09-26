# API reference

The Lead Management API is a JSON REST API built with Django REST Framework. The OpenAPI 3 schema is committed as [`backend/schema.yml`](../backend/schema.yml) and served live:

| | |
| --- | --- |
| Interactive docs (Swagger UI) | `/api/docs/` |
| ReDoc | `/api/redoc/` |
| OpenAPI schema | `/api/schema/` |

Every example below uses `http://127.0.0.1:8000`. On the [live demo](https://lead-platform-c3mw.onrender.com/) the same paths work under `https://lead-platform-c3mw.onrender.com`.

## Conventions

- **JSON in, JSON out.** Send `Content-Type: application/json`.
- **Authentication:** `Authorization: Bearer <access token>` on every endpoint except login, refresh and the public lead form.
- **Errors:** authentication, permission and not-found errors return `{"detail": "..."}`. Validation errors return an object keyed by field, for example `{"phone": ["Phone number must contain only digits."]}`, or `{"status": "Cannot change status from New to Won."}`.
- **Pagination:** list endpoints return `{"count", "next", "previous", "results"}`, 20 items per page by default. Use `?page=N` and `?page_size=N` (maximum 100).
- **Timestamps** are ISO 8601 in UTC. Every record has `created_at` and `updated_at`.

## Roles and access

Every user is either an **Admin** or a **Member**. The first account created with `ensure_superuser` is an Admin. Admins add further users in Django admin at `/admin/`.

| Action | Admin | Member |
| --- | --- | --- |
| See leads | All leads | Leads they created or are assigned to |
| Create a lead | Yes | Yes (they become its creator) |
| Edit lead details | Any lead | Leads they created or are assigned to |
| Delete a lead | Yes | No |
| Change a lead's status | Any lead | Leads they created or are assigned to |
| Assign a lead | Yes | No |
| Add notes, read notes and activities | Any lead | Leads they created or are assigned to |
| Edit or delete a note | Any note | Notes they wrote |

A lead a member cannot see answers `404 Not Found`, not `403`, so the API doesn't reveal that it exists.

## Authentication

Tokens are JWTs:
- **Access tokens** last 15 minutes.
- **Refresh tokens** last 7 days and are **rotated**. Each refresh returns a new refresh token, and the one you sent is blacklisted, so it can't be used again.

### Log in

`POST /api/auth/login/`

```sh
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H 'Content-Type: application/json' \
  -d '{"email": "admin@example.com", "password": "..."}'
```

```json
{ "access": "eyJ...", "refresh": "eyJ..." }
```

Wrong credentials return `401` with `{"detail": "No active account found with the given credentials"}`.

### Refresh

`POST /api/auth/refresh/` with `{"refresh": "..."}` returns a new `access` **and** a new `refresh` token. Store both. Reusing the old refresh token returns `401` (`Token is blacklisted`).

### Log out

`POST /api/auth/logout/` with `{"refresh": "..."}`, authenticated. It blacklists the refresh token and returns `205 Reset Content`.

### Current user

`GET /api/auth/me/` returns `{"id", "email", "first_name", "last_name", "role"}`, where `role` is `ADMIN` or `MEMBER`.

### Assignable members

`GET /api/auth/users/` returns a paginated list of active Members as `{"id", "full_name"}`, ordered by name. It is used to fill the assignment picker.

## Leads

A lead:

```json
{
  "id": 7,
  "first_name": "Ada",
  "last_name": "Lovelace",
  "email": "ada@example.com",
  "phone": "5550100",
  "company": "Engines Ltd",
  "source": "Referral",
  "status": "QUALIFIED",
  "created_by": { "id": 1, "full_name": "Alice Admin" },
  "assigned_to": { "id": 2, "full_name": "Bob Member" },
  "created_at": "2026-09-26T10:00:00Z",
  "updated_at": "2026-09-26T12:30:00Z"
}
```

- `created_by` is `null` for leads submitted through the public form.
- `assigned_to` is `null` until someone assigns the lead.
- `phone` may only contain digits (an optional leading `+` is allowed).

### List

`GET /api/leads/` returns the leads visible to you, newest first.

| Parameter | Effect |
| --- | --- |
| `status` | `NEW`, `CONTACTED`, `QUALIFIED`, `PROPOSAL`, `WON` or `LOST` |
| `assigned_to`, `created_by` | A user id |
| `company` | Exact company name |
| `search` | Case-insensitive match on first name, last name, email, phone or company |
| `ordering` | `created_at`, `updated_at`, `first_name`, `last_name` or `status`; prefix `-` for descending |
| `page`, `page_size` | Pagination |

```sh
curl -H "Authorization: Bearer $ACCESS" \
  "http://127.0.0.1:8000/api/leads/?status=QUALIFIED&search=acme&ordering=-updated_at"
```

### Create

`POST /api/leads/` with `first_name`, `last_name` and `email` (required), plus optional `phone`, `company` and `source`.

- New leads always start in `NEW`, unassigned, with you as `created_by`.
- A **Created** activity is recorded.
- The response is `201` with the full lead.

### Retrieve, edit, delete

- `GET /api/leads/{id}/` returns one lead.
- `PATCH /api/leads/{id}/` changes some of the contact fields; `PUT` replaces all of them. A `status`, `assigned_to` or `created_by` field in the body is ignored: status and assignment have their own endpoints below. An edit that changes a value records an **Updated** activity naming the changed fields, for example "Bob Member updated company and source." An edit that changes nothing records nothing.
- `DELETE /api/leads/{id}/` deletes a lead, together with its notes and activities. Admins only. Returns `204`.

### Public form

`POST /api/leads/public/` takes the same fields as creating a lead, with **no authentication**. The website's enquiry form uses it.

- The lead gets `created_by: null`.
- Its activity reads "Lead submitted through the public form."
- Submissions are **rate-limited per client** (`PUBLIC_LEADS_RATE`, default `20/hour`). Past the limit it returns `429 Too Many Requests`.

## The status pipeline

Status only moves forward through the pipeline. From any open stage it can go to `LOST`. `WON` and `LOST` are final.

```text
NEW ──▶ CONTACTED ──▶ QUALIFIED ──▶ PROPOSAL ──▶ WON
 │          │             │             │
 └──────────┴─────────────┴─────────────┴──────▶ LOST
```

`POST /api/leads/{id}/status/` with `{"status": "CONTACTED"}`:

- **Allowed:** it returns `200` with the updated lead and records a **Status Changed** activity, for example "Status changed from New to Contacted by Bob Member."
- **Not allowed:** it returns `400` with the reason, for example `{"status": "Cannot change status from New to Won."}` or `{"status": "Lead is already in this status."}`.

The rules live in one place (`apps/leads/constants.py`) and are enforced by the service layer. No other endpoint can change a lead's status.

## Assignment

`POST /api/leads/{id}/assign/` with `{"assigned_to": <user id>}`. Admins only. The user must be active.

It returns `200` with the updated lead and records an **Assigned** activity, for example "Lead assigned to Bob Member by Alice Admin." Assigning a lead gives that member access to it.

## Notes

| Endpoint | Does |
| --- | --- |
| `POST /api/leads/{id}/notes/` | Adds a note (`{"content": "..."}`). Returns `201` and records a **Note Added** activity |
| `GET /api/leads/{id}/notes/list/` | Returns all notes for a lead as an array, newest first, each with its `author` |
| `PATCH` or `PUT /api/leads/notes/{id}/` | Changes a note's `content`. Its author or an Admin only |
| `DELETE /api/leads/notes/{id}/` | Deletes a note. Its author or an Admin only. Returns `204` |

## Activity timeline

`GET /api/leads/{id}/activities/` returns everything that happened to a lead as an array, newest first:

```json
[
  {
    "id": 12,
    "lead": 7,
    "user": { "id": 2, "full_name": "Bob Member" },
    "activity_type": "STATUS_CHANGED",
    "description": "Status changed from Contacted to Qualified by Bob Member.",
    "created_at": "2026-09-26T12:30:00Z",
    "updated_at": "2026-09-26T12:30:00Z"
  }
]
```

| `activity_type` | Recorded when |
| --- | --- |
| `CREATED` | A lead is created, in the app or through the public form (`user` is `null` for the form) |
| `UPDATED` | A lead's contact details change |
| `STATUS_CHANGED` | A status change succeeds |
| `ASSIGNED` | A lead is assigned |
| `NOTE_ADDED` | A note is added |

Activities are written only by the service functions in `apps/leads/services.py`, in the same database transaction as the change they describe. If the change fails, no activity is recorded, and no change is saved without its activity.

## Status codes

| Code | Meaning |
| --- | --- |
| `200` / `201` / `204` / `205` | Success (read or update / created / deleted / logged out) |
| `400` | Invalid input or a disallowed status change; the body says which field and why |
| `401` | Missing, expired or blacklisted token, or wrong credentials |
| `403` | Signed in, but your role can't do this (for example a Member assigning or deleting) |
| `404` | The lead or note doesn't exist, or you aren't allowed to see it |
| `429` | The public form's rate limit was reached |
