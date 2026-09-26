# ==============================================================================
# ensure_superuser Command Tests
# ==============================================================================

import os
from io import StringIO
from unittest import mock

from apps.accounts.choices import UserRole
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

User = get_user_model()

ENV = {
    "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
    "DJANGO_SUPERUSER_PASSWORD": "a-strong-demo-password",
    "DJANGO_SUPERUSER_FIRST_NAME": "Ada",
    "DJANGO_SUPERUSER_LAST_NAME": "Admin",
}


def run(env: dict[str, str]) -> str:
    """Run the command with the given DJANGO_SUPERUSER_* variables added."""

    out = StringIO()

    with mock.patch.dict(os.environ, env):
        call_command("ensure_superuser", stdout=out)

    return out.getvalue()


class EnsureSuperuserTests(TestCase):
    """Verify the admin bootstrap is safe to run on every start."""

    def setUp(self) -> None:
        # Start each test without any DJANGO_SUPERUSER_* variables
        patcher = mock.patch.dict(os.environ)
        patcher.start()
        self.addCleanup(patcher.stop)

        for name in ENV:
            os.environ.pop(name, None)

    def test_skips_when_not_configured(self) -> None:
        """Ensure nothing happens without the variables."""

        output = run({})

        self.assertIn("skipping", output)
        self.assertFalse(User.objects.exists())

    def test_creates_admin_once(self) -> None:
        """Ensure the account is created with the Admin role and a working password."""

        output = run(ENV)

        user = User.objects.get(email="admin@example.com")
        self.assertIn("created admin", output)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.role, UserRole.ADMIN)
        self.assertEqual((user.first_name, user.last_name), ("Ada", "Admin"))
        self.assertTrue(user.check_password("a-strong-demo-password"))

    def test_rerun_leaves_existing_account_unchanged(self) -> None:
        """Ensure a restart never resets a password changed after creation."""

        run(ENV)
        user = User.objects.get(email="admin@example.com")
        user.set_password("changed-later")
        user.save()

        output = run({**ENV, "DJANGO_SUPERUSER_EMAIL": "ADMIN@example.com"})

        user.refresh_from_db()
        self.assertIn("already exists", output)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(user.check_password("changed-later"))

    def test_half_configured_is_an_error(self) -> None:
        """Ensure an email without a password fails loudly instead of skipping."""

        with self.assertRaisesMessage(CommandError, "DJANGO_SUPERUSER_PASSWORD"):
            run({"DJANGO_SUPERUSER_EMAIL": "admin@example.com"})
