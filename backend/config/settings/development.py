# ==============================================================================
# Development Settings : version 1.0.0
# ==============================================================================

from typing import TYPE_CHECKING

from . import base
from .auth import *
from .base import *
from .database import *
from .rest import *
from .spectacular import *

if TYPE_CHECKING:
    INSTALLED_APPS: list[str]
    MIDDLEWARE: list[str]
    TEMPLATES: list[dict]
    LOGGING: dict

DEBUG = True

INSTALLED_APPS = [
    *base.INSTALLED_APPS,
    "debug_toolbar",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    *base.MIDDLEWARE,
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
