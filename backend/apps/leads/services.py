# ==============================================================================
# Lead Business Services
# ==============================================================================

from apps.accounts.models import User
from apps.leads.choices import ActivityType
from apps.leads.models import Lead, LeadActivity
from django.db import transaction


@transaction.atomic
def assign_lead(
    *,
    lead: Lead,
    assigned_to: User,
    performed_by: User,
) -> Lead:
    """
    Assign a lead to a member and record the activity.
    """

    lead.assigned_to = assigned_to
    lead.save(
        update_fields=[
            "assigned_to",
            "updated_at",
        ]
    )

    LeadActivity.objects.create(
        lead=lead,
        user=performed_by,
        activity_type=ActivityType.ASSIGNED,
        description=(f"Lead assigned to {assigned_to.get_full_name()} " f"by {performed_by.get_full_name()}."),
    )

    return lead
