# ==============================================================================
# Model for the User entity
# ==============================================================================

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.common.models import Base

from .choices import UserRole
from .managers import UserManager


class User(Base, AbstractBaseUser, PermissionsMixin):
    """Represent a user authenticated by a unique email address."""

    email = models.EmailField(
        unique=True,
    )

    first_name = models.CharField(
        max_length=55,
    )

    last_name = models.CharField(
        max_length=55,
    )

    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.MEMBER,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
    ]

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        """Return the user's full name for Django integrations."""

        return self.full_name

    def get_short_name(self) -> str:
        """Return the user's first name for Django integrations."""

        return self.first_name

    @property
    def full_name(self) -> str:
        """Return the user's combined first and last name."""

        return f"{self.first_name} {self.last_name}".strip()

    @property
    def is_admin(self) -> bool:
        """Return whether the user has the administrator role."""

        return self.role == UserRole.ADMIN

    @property
    def is_member(self) -> bool:
        """Return whether the user has the member role."""

        return self.role == UserRole.MEMBER
