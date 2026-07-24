# Lead Management Platform

A production-ready Lead Management Platform built with **Django REST Framework** and **React**.

The platform enables sales teams to capture, manage, assign, and track leads throughout the sales pipeline. It features JWT authentication, role-based access control, activity tracking, comprehensive API documentation, and a scalable architecture.

This project is being developed as part of the **Full Stack Development Assessment**.

---

## Features

### Authentication

- JWT Authentication
- Login, Logout & Token Refresh
- Current User endpoint
- Password hashing
- Protected REST API

### Lead Management

- Create, retrieve, update and delete leads
- Lead assignment
- Lead status management
- Notes and activity history
- Server-side validation

### API

- RESTful API
- OpenAPI 3 specification
- Swagger UI
- ReDoc documentation
- Standardised API responses

### Architecture

- Modular Django application structure
- Environment-based configuration
- PostgreSQL database
- Custom User model
- Shared serializers and API documentation components

---

## Technology Stack

### Backend

- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- drf-spectacular

### Frontend

- React
- Vite
- Axios
- React Router

---

## Project Structure

```text
backend/
├── config/
├── apps/
│   ├── accounts/
│   ├── common/
│   └── leads/
└── manage.py

frontend/
```

---

## API Documentation

Once the backend is running, documentation is available at:

| Service        | URL            |
| -------------- | -------------- |
| Swagger UI     | `/api/docs/`   |
| ReDoc          | `/api/redoc/`  |
| OpenAPI Schema | `/api/schema/` |

---

## Authentication

All protected endpoints require a JWT access token.

Example:

```http
Authorization: Bearer <access_token>
```

Authentication endpoints:

```http
POST /api/auth/login/
POST /api/auth/refresh/
POST /api/auth/logout/
GET  /api/auth/me/
```

---

## Running Locally

### Clone the repository

```bash
git clone <repository-url>
cd lead-management-platform
```

### Create a virtual environment

```bash
python -m venv .venv
```

### Activate the environment

**Windows**

```powershell
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Configure environment variables

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

### Apply migrations

```bash
python manage.py migrate
```

### Create a superuser

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

---

## Testing

Run all tests:

```bash
python manage.py test
```

Run a specific app:

```bash
python manage.py test apps.accounts
python manage.py test apps.leads
```

---

## Project Status

### Completed

- Project setup
- JWT Authentication
- User management
- Lead CRUD
- Notes & Activity models
- Django Admin
- OpenAPI documentation
- Unit tests

### In Progress

- Filtering & Search
- Business endpoints
- Role-based permissions
- Frontend dashboard
- Deployment

---

## Roadmap

- Advanced lead filtering
- Assignment workflow
- Status workflow
- Activity timeline
- Dashboard analytics
- CSV export
- Email notifications
- Docker support
- GitHub Actions CI/CD

---

## License

This project is licensed under the MIT License.
