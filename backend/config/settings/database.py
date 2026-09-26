# ==============================================================================
# PostgreSQL Database Configuration
# ==============================================================================
import dj_database_url
from decouple import config
from django.core.exceptions import ImproperlyConfigured

DATABASE_URL = config(
    "DATABASE_URL",
    default="",
    cast=str,
)

# Without this, Django starts and only fails on first database access with a
# misleading "supply the ENGINE value" error
if not DATABASE_URL:
    raise ImproperlyConfigured(
        "DATABASE_URL must be set, e.g. postgres://user:password@localhost:5432/dbname (see .env.example)."
    )

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    ),
}
