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


def load_production_settings(code: str = "", **overrides: str) -> subprocess.CompletedProcess[str]:
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
        [sys.executable, "-c", f"import config.settings as s\n{code}"],
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


class HstsSettingsTests(SimpleTestCase):
    """Verify HSTS defaults are conservative and configurable from the environment."""

    PRINT_HSTS = "print(s.SECURE_HSTS_SECONDS, s.SECURE_HSTS_INCLUDE_SUBDOMAINS, s.SECURE_HSTS_PRELOAD)"

    def test_defaults_are_conservative(self) -> None:
        """Ensure HSTS defaults to one hour without subdomains or preload."""

        result = load_production_settings(self.PRINT_HSTS)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.split(), ["3600", "False", "False"])

    def test_environment_overrides(self) -> None:
        """Ensure each HSTS setting can be raised from the environment."""

        result = load_production_settings(
            self.PRINT_HSTS,
            HSTS_SECONDS="31536000",
            HSTS_INCLUDE_SUBDOMAINS="True",
            HSTS_PRELOAD="True",
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.split(), ["31536000", "True", "True"])
