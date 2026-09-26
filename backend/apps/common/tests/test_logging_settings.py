# ==============================================================================
# Production Logging Tests
# ==============================================================================

import os
import subprocess
import sys
from pathlib import Path

from django.test import SimpleTestCase

BACKEND_DIR = Path(__file__).resolve().parents[3]

EMIT_LOGS = """
import logging
import django

django.setup()

try:
    raise ValueError("boom")
except ValueError:
    logging.getLogger("django.request").exception("Internal Server Error: /api/leads/")

logging.getLogger("apps.leads").info("lead created")
logging.getLogger("apps.leads").debug("noisy detail")
"""


def run_production(**overrides: str) -> subprocess.CompletedProcess[str]:
    """Emit sample logs from a fresh interpreter using the production settings."""

    env = {
        **os.environ,
        "DJANGO_SETTINGS_MODULE": "config.settings",
        "DJANGO_ENV": "production",
        "DEBUG": "False",
        "SECRET_KEY": "test-only-secret-key-for-logging-settings-checks",
        "DATABASE_URL": "sqlite:///:memory:",
        "ALLOWED_HOSTS": "api.example.com",
        "CORS_ALLOWED_ORIGINS": "https://app.example.com",
        "CSRF_TRUSTED_ORIGINS": "https://app.example.com",
        **overrides,
    }

    return subprocess.run(
        [sys.executable, "-c", EMIT_LOGS],
        cwd=BACKEND_DIR,
        env=env,
        capture_output=True,
        text=True,
    )


class ProductionLoggingTests(SimpleTestCase):
    """Verify production writes errors and app logs to the console."""

    def test_request_errors_are_logged_with_traceback(self) -> None:
        """Ensure a 500's traceback reaches the container log."""

        result = run_production()

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ERROR django.request: Internal Server Error: /api/leads/", result.stderr)
        self.assertIn("ValueError: boom", result.stderr)

    def test_app_info_logs_respect_log_level(self) -> None:
        """Ensure app logs appear at INFO by default and LOG_LEVEL can raise the bar."""

        default = run_production()
        quiet = run_production(LOG_LEVEL="WARNING")

        self.assertIn("INFO apps.leads: lead created", default.stderr)
        self.assertNotIn("noisy detail", default.stderr)
        self.assertNotIn("lead created", quiet.stderr)
