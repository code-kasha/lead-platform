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

# Off only to try the production image locally over plain HTTP
SECURE_SSL_REDIRECT = config(
    "SECURE_SSL_REDIRECT",
    default=True,
    cast=bool,
)

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

# ==============================================================================
# Logging
# ==============================================================================

# Django's defaults only log to the console when DEBUG is on and otherwise
# email ADMINS (none are set), so production errors, including 500
# tracebacks, were silently dropped. Write everything to stderr, which
# container platforms collect.
LOG_LEVEL = config("LOG_LEVEL", default="INFO").upper()

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain": {
            "format": "{asctime} {levelname} {name}: {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        # Replace Django's handlers (debug-only console, mail_admins) with the
        # root console handler; request errors always get through.
        "django": {
            "handlers": [],
            "level": "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": [],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

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

# Render sets RENDER_EXTERNAL_HOSTNAME to the service's public host. With the
# frontend served from the same origin, that host is all three lists need, so
# use it for any list left unset. Explicit values always win.
RENDER_EXTERNAL_HOSTNAME = config("RENDER_EXTERNAL_HOSTNAME", default="")

if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS = ALLOWED_HOSTS or [RENDER_EXTERNAL_HOSTNAME]
    CORS_ALLOWED_ORIGINS = CORS_ALLOWED_ORIGINS or [f"https://{RENDER_EXTERNAL_HOSTNAME}"]
    CSRF_TRUSTED_ORIGINS = CSRF_TRUSTED_ORIGINS or [f"https://{RENDER_EXTERNAL_HOSTNAME}"]

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

# ==============================================================================
# Static Files
# ==============================================================================

# Compressed copies are written by collectstatic at image build time
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Serve the built frontend's files (assets/, favicon.svg) from the site root
if FRONTEND_DIST.is_dir():
    WHITENOISE_ROOT = FRONTEND_DIST


def _is_hashed_asset(path: str, url: str) -> bool:
    """Vite's assets/ files have content hashes in their names, so they can be cached forever."""

    return url.startswith("/assets/")


WHITENOISE_IMMUTABLE_FILE_TEST = _is_hashed_asset
