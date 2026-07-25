# ==============================================================================
# PostgreSQL Database Configuration
# ==============================================================================
import dj_database_url
from decouple import config

DATABASE_URL = config(
    "DATABASE_URL",
    default="",
    cast=str,
)

DATABASES = {
    "default": dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True,
    ),
}
