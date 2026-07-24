# ==============================================================================
# Models for the leads app
# ==============================================================================

from apps.common.models import Base
from django.conf import settings
from django.db import models

from .choices import LeadStatus
from .validators import validate_phone


class Lead(Base):
    first_name = models.CharField(max_length=55)

    last_name = models.CharField(max_length=55)

    email = models.EmailField()

    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[validate_phone],
    )

    company = models.CharField(
        max_length=100,
        blank=True,
    )

    source = models.CharField(
        max_length=50,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=LeadStatus.choices,
        default=LeadStatus.NEW,
    )

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_leads",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
