from apps.common.models import Base
from django.db import models

from .choices import UserRole


class User(Base):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    role = models.CharField(
        max_length=10,
        choices=UserRole.choices,
        default=UserRole.MEMBER,
    )
    is_active = models.BooleanField(default=True)
