# ==============================================================================
# Production Settings : version 1.0.0
# ==============================================================================

from decouple import config

from .auth import *
from .base import *
from .database import *
from .rest import *
from .spectacular import *

DEBUG = False

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    cast=lambda value: [item.strip() for item in value.split(",")],
    default=[],
)

CSRF_TRUSTED_ORIGINS = config(
    "CSRF_TRUSTED_ORIGINS",
    cast=lambda value: [item.strip() for item in value.split(",")],
    default=[],
)
