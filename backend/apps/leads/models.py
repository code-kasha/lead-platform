# ==============================================================================
# Models for the leads app
# ==============================================================================

from apps.common.models import Base
from django.conf import settings
from django.db import models

from .choices import ActivityType, LeadStatus
from .validators import validate_phone


class Lead(Base):
    """Store contact information and workflow state for a sales lead."""

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


class LeadNote(Base):
    """Store a note associated with a lead."""

    lead = models.ForeignKey(
        "Lead",
        on_delete=models.CASCADE,
        related_name="notes",
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="lead_notes",
    )

    content = models.TextField()

    class Meta:
        db_table = "lead_notes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Note by {self.author} on {self.lead}"


class LeadActivity(Base):
    """Record an auditable event in a lead's lifecycle."""

    lead = models.ForeignKey(
        "Lead",
        on_delete=models.CASCADE,
        related_name="activities",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="lead_activities",
    )

    activity_type = models.CharField(
        max_length=30,
        choices=ActivityType.choices,
    )

    description = models.TextField()

    class Meta:
        db_table = "lead_activities"
        ordering = ["-created_at"]
        verbose_name = "Lead Activity"
        verbose_name_plural = "Lead Activities"

    def __str__(self):
        return f"{self.activity_type} - {self.lead}"
