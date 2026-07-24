from apps.common.models import Base
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from .choices import UserRole
from .managers import UserManager


class User(Base, AbstractBaseUser, PermissionsMixin):
    """
    Custom user model using email as the unique identifier.
    """

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

    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def get_full_name(self):
        return f"{self.full_name}"

    @property
    def get_short_name(self):
        return f"{self.first_name}"

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    @property
    def is_member(self):
        return self.role == UserRole.MEMBER
