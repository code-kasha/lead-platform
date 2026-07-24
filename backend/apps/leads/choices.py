# ==============================================================================
# Choices for the Lead model
# ==============================================================================

from django.db import models


class LeadStatus(models.TextChoices):
    NEW = "NEW", "New"
    CONTACTED = "CONTACTED", "Contacted"
    QUALIFIED = "QUALIFIED", "Qualified"
    PROPOSAL = "PROPOSAL", "Proposal"
    WON = "WON", "Won"
    LOST = "LOST", "Lost"


class ActivityType(models.TextChoices):
    CREATED = "CREATED", "Created"
    STATUS_CHANGED = "STATUS_CHANGED", "Status Changed"
    ASSIGNED = "ASSIGNED", "Assigned"
    NOTE_ADDED = "NOTE_ADDED", "Note Added"
    UPDATED = "UPDATED", "Updated"
