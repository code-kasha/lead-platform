# ==============================================================================
# Choices for the User model
# ==============================================================================

from django.db import models


class UserRole(models.TextChoices):
    ADMIN = "ADMIN", "Admin"
    MEMBER = "MEMBER", "Member"
