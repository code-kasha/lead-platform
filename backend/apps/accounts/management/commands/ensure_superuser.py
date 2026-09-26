# ==============================================================================
# Create the first admin account from environment variables
# ==============================================================================

import os
from typing import Any

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

REQUIRED = ("DJANGO_SUPERUSER_EMAIL", "DJANGO_SUPERUSER_PASSWORD")


class Command(BaseCommand):
    """Create an admin from DJANGO_SUPERUSER_* variables if it doesn't exist.

    Runs on every container start (hosts without a shell can't run
    createsuperuser). An existing account is left untouched, so a changed
    password is never overwritten by the environment.
    """

    help = "Create the admin account from DJANGO_SUPERUSER_* environment variables, once."

    def handle(self, *args: Any, **options: Any) -> None:
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not email and not password:
            self.stdout.write("ensure_superuser: DJANGO_SUPERUSER_EMAIL not set, skipping.")
            return

        missing = [name for name in REQUIRED if not os.environ.get(name, "").strip()]
        if missing:
            raise CommandError(f"ensure_superuser: set {' and '.join(missing)}.")

        User = get_user_model()

        if User.objects.filter(email__iexact=email).exists():
            self.stdout.write(f"ensure_superuser: {email} already exists, leaving it unchanged.")
            return

        User.objects.create_superuser(
            email=email,
            password=password,
            first_name=os.environ.get("DJANGO_SUPERUSER_FIRST_NAME", "Admin"),
            last_name=os.environ.get("DJANGO_SUPERUSER_LAST_NAME", "User"),
        )

        self.stdout.write(self.style.SUCCESS(f"ensure_superuser: created admin {email}."))
