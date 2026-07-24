# ==============================================================================
# Choices for the User model
# ==============================================================================

from django.db import models


class UserRole(models.TextChoices):
    """Define the roles available to user accounts."""

    ADMIN = "ADMIN", "Admin"
    MEMBER = "MEMBER", "Member"
