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

CORS_ALLOWED_ORIGINS = get_list("CORS_ALLOWED_ORIGINS")

CSRF_TRUSTED_ORIGINS = get_list("CSRF_TRUSTED_ORIGINS")

SECURE_PROXY_SSL_HEADER = (
    "HTTP_X_FORWARDED_PROTO",
    "https",
)
