# ==============================================================================
# Development Settings : version 1.0.0
# ==============================================================================

from .auth import *
from .base import *
from .database import *
from .rest import *
from .spectacular import *

# ==============================================================================
# This following database configuration is for development purposes only.
# It uses SQLite as the database engine, which is suitable for local development and testing.
# In a production environment, you should use a more robust database system such as PostgreSQL or MySQL.
# ==============================================================================

# DATABASES = {
#    "default": {
#        "ENGINE": "django.db.backends.sqlite3",
#        "NAME": BASE_DIR / "db.sqlite3",  # noqa: F405
#    }
# }

DEBUG = True

INSTALLED_APPS += [  # noqa: F405
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *MIDDLEWARE,  # noqa: F405
]
