# ==============================================================================
# Initialize Django settings for the active environment
# ==============================================================================

from typing import cast

from decouple import config

ENV = cast(str, config("DJANGO_ENV", default="development")).lower()

if ENV == "production":
    from .production import *
else:
    from .development import *
