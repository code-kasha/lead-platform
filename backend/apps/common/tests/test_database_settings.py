# ==============================================================================
# Database Settings Tests
# ==============================================================================

import os
import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase

BACKEND_DIR = Path(__file__).resolve().parents[3]


def load_settings(database_url: str) -> subprocess.CompletedProcess[str]:
    """Import the settings package in a fresh interpreter with the given DATABASE_URL."""

    env = {
        **os.environ,
        "DJANGO_ENV": "development",
        "SECRET_KEY": "test-only-secret-key-for-database-settings-checks",
        # An explicit empty value overrides any DATABASE_URL in a local .env
        "DATABASE_URL": database_url,
    }

    return subprocess.run(
        [sys.executable, "-c", "import config.settings as s; print(s.DATABASES['default']['ENGINE'])"],
        cwd=BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
    )


class DatabaseSettingsTests(SimpleTestCase):
    """Verify startup fails clearly without a database URL."""

    def test_missing_database_url_raises(self) -> None:
        """Ensure an empty DATABASE_URL stops startup and names the variable."""

        result = load_settings("")

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("ImproperlyConfigured", result.stderr)
        self.assertIn("DATABASE_URL must be set", result.stderr)

    def test_database_url_selects_engine(self) -> None:
        """Ensure a provided DATABASE_URL configures the matching engine."""

        result = load_settings("sqlite:///:memory:")

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "django.db.backends.sqlite3")
