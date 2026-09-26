# ==============================================================================
# Production Settings : version 1.0.0
# ==============================================================================

from decouple import config
from django.core.exceptions import ImproperlyConfigured

from .auth import *
from .base import *
from .database import *
from .rest import *
from .spectacular import *

DEBUG = config(
    "DEBUG",
    default=False,
    cast=bool,
)

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# ==============================================================================
# HTTP Strict Transport Security
# ==============================================================================

# Conservative default: browsers remember "HTTPS only" for one hour. Once HTTPS
# is confirmed stable, raise HSTS_SECONDS in steps (e.g. 86400, then 31536000).
# Enable subdomains/preload only if every subdomain serves HTTPS: preload list
# removal takes months.
SECURE_HSTS_SECONDS = config(
    "HSTS_SECONDS",
    default=3600,
    cast=int,
)

SECURE_HSTS_INCLUDE_SUBDOMAINS = config(
    "HSTS_INCLUDE_SUBDOMAINS",
    default=False,
    cast=bool,
)

SECURE_HSTS_PRELOAD = config(
    "HSTS_PRELOAD",
    default=False,
    cast=bool,
)

CORS_ALLOWED_ORIGINS = get_list("CORS_ALLOWED_ORIGINS")

CSRF_TRUSTED_ORIGINS = get_list("CSRF_TRUSTED_ORIGINS")

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)

# ==============================================================================
# Required Environment
# ==============================================================================

# Empty lists fail silently at runtime (400s, or browsers blocking every API
# call), so refuse to start instead.
for _name in ("ALLOWED_HOSTS", "CORS_ALLOWED_ORIGINS", "CSRF_TRUSTED_ORIGINS"):
    if not globals()[_name]:
        raise ImproperlyConfigured(f"{_name} must be set in production (comma-separated list).")

# ==============================================================================

MIDDLEWARE.insert(
    2,
    "whitenoise.middleware.WhiteNoiseMiddleware",
)
