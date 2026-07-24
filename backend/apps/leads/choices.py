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
