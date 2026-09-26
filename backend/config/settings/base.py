# ==============================================================================
# Base Settings - version 1.0.0
# ==============================================================================

from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ==============================================================================
# Environment Helpers
# ==============================================================================


def get_list(name: str) -> list[str]:
    """Return a comma-separated environment variable as a list."""

    value = config(
        name,
        default="",
    )

    return [item.strip() for item in value.split(",") if item.strip()]


SECRET_KEY = config("SECRET_KEY")

ALLOWED_HOSTS = get_list("ALLOWED_HOSTS")

# ==============================================================================
# Applications
# ==============================================================================

DJANGO_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "django_extensions",
    "django_filters",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_spectacular",
    "drf_spectacular_sidecar",
]

LOCAL_APPS = [
    "apps.accounts",
    "apps.common",
    "apps.leads",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# ==============================================================================
# Middleware
# ==============================================================================

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ==============================================================================
# URLs
# ==============================================================================

ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


# ==============================================================================
# Templates
# ==============================================================================

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


# ==============================================================================
# Internationalization
# ==============================================================================

LANGUAGE_CODE = "en-IN"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


# ==============================================================================
# Static & Media Files
# ==============================================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = []

static_dir = BASE_DIR / "static"

if static_dir.exists():
    STATICFILES_DIRS.append(static_dir)

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"


# ==============================================================================
# Default Primary Key
# ==============================================================================

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
