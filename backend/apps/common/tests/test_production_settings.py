# ==============================================================================
# Production Settings Tests
# ==============================================================================

import os
import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase

BACKEND_DIR = Path(__file__).resolve().parents[3]

REQUIRED_LISTS = (
    "ALLOWED_HOSTS",
    "CORS_ALLOWED_ORIGINS",
    "CSRF_TRUSTED_ORIGINS",
)


def load_production_settings(**overrides: str) -> subprocess.CompletedProcess[str]:
    """Import the settings package in a fresh interpreter with DJANGO_ENV=production."""

    env = {
        **os.environ,
        "DJANGO_ENV": "production",
        "DEBUG": "False",
        "SECRET_KEY": "test-only-secret-key-for-production-settings-checks",
        "DATABASE_URL": "sqlite:///:memory:",
        "ALLOWED_HOSTS": "api.example.com",
        "CORS_ALLOWED_ORIGINS": "https://app.example.com",
        "CSRF_TRUSTED_ORIGINS": "https://app.example.com",
        **overrides,
    }

    return subprocess.run(
        [sys.executable, "-c", "import config.settings"],
        cwd=BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
    )


class ProductionSettingsTests(SimpleTestCase):
    """Verify production refuses to start without required host/origin lists."""

    def test_loads_when_required_lists_are_set(self) -> None:
        """Ensure production settings import cleanly with all lists present."""

        result = load_production_settings()

        self.assertEqual(result.returncode, 0, result.stderr)

    def test_missing_required_list_raises(self) -> None:
        """Ensure each required list, when empty, stops startup with a clear error."""

        for name in REQUIRED_LISTS:
            with self.subTest(name=name):
                result = load_production_settings(**{name: ""})

                self.assertNotEqual(result.returncode, 0)
                self.assertIn("ImproperlyConfigured", result.stderr)
                self.assertIn(f"{name} must be set in production", result.stderr)
