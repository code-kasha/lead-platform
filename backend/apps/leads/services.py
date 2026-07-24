# ==============================================================================
# Lead Business Services
# ==============================================================================

from apps.accounts.models import User
from apps.leads.choices import ActivityType, LeadStatus
from apps.leads.constants import ALLOWED_STATUS_TRANSITIONS
from apps.leads.models import Lead, LeadActivity, LeadNote
from django.db import transaction
from rest_framework.exceptions import ValidationError


@transaction.atomic
def add_lead_note(
    *,
    lead: Lead,
    content: str,
    author: User,
) -> LeadNote:
    """
    Create a note for a lead and record the activity.
    """

    note = LeadNote.objects.create(
        lead=lead,
        content=content,
        author=author,
    )

    LeadActivity.objects.create(
        lead=lead,
        user=author,
        activity_type=ActivityType.NOTE_ADDED,
        description=f"{author.get_full_name()} added a note.",
    )

    return note


@transaction.atomic
def change_lead_status(
    *,
    lead: Lead,
    status: str,
    performed_by: User,
) -> Lead:
    """
    Change the status of a lead and record the activity.
    """

    current_status = LeadStatus(lead.status)
    new_status = LeadStatus(status)

    if current_status == new_status:
        raise ValidationError(
            {
                "status": "Lead is already in this status.",
            }
        )

    allowed = ALLOWED_STATUS_TRANSITIONS.get(
        current_status,
        set(),
    )

    if new_status not in allowed:
        raise ValidationError(
            {"status": (f"Cannot change status from " f"{current_status.label} " f"to " f"{new_status.label}.")}
        )

    lead.status = new_status

    lead.save(
        update_fields=[
            "status",
            "updated_at",
        ],
    )

    LeadActivity.objects.create(
        lead=lead,
        user=performed_by,
        activity_type=ActivityType.STATUS_CHANGED,
        description=(
            f"Status changed from "
            f"{current_status.label} "
            f"to "
            f"{new_status.label} "
            f"by "
            f"{performed_by.get_full_name()}."
        ),
    )

    return lead


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
        ],
    )

    LeadActivity.objects.create(
        lead=lead,
        user=performed_by,
        activity_type=ActivityType.ASSIGNED,
        description=(f"Lead assigned to " f"{assigned_to.get_full_name()} " f"by " f"{performed_by.get_full_name()}."),
    )

    return lead
