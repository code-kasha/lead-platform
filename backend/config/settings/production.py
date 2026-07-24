# ==============================================================================
# Production Settings : version 1.0.0
# ==============================================================================

from .auth import *
from .base import *
from .database import *
from .rest import *
from .spectacular import *

DEBUG = False

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True
