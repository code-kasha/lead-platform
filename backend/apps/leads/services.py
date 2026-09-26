# ==============================================================================
# Lead Business Services
# ==============================================================================

from typing import Any

from apps.accounts.models import User
from apps.leads.choices import ActivityType, LeadStatus
from apps.leads.constants import ALLOWED_STATUS_TRANSITIONS
from apps.leads.models import Lead, LeadActivity, LeadNote
from django.db import transaction
from rest_framework.exceptions import ValidationError


@transaction.atomic
def create_lead(
    *,
    data: dict[str, Any],
    created_by: User | None,
) -> Lead:
    """Create a lead in the NEW status and record its creation activity.

    `created_by` is None for leads submitted through the public form.
    """

    lead = Lead.objects.create(
        **data,
        created_by=created_by,
    )

    description = (
        f"Lead created by {created_by.get_full_name()}."
        if created_by is not None
        else "Lead submitted through the public form."
    )

    LeadActivity.objects.create(
        lead=lead,
        user=created_by,
        activity_type=ActivityType.CREATED,
        description=description,
    )

    return lead


@transaction.atomic
def update_lead(
    *,
    lead: Lead,
    data: dict[str, Any],
    performed_by: User,
) -> Lead:
    """Apply field changes to a lead and record which fields changed.

    Status and assignment have their own services; an update that changes
    nothing is saved as a no-op and records no activity.
    """

    changed = [field for field, value in data.items() if getattr(lead, field) != value]

    if not changed:
        return lead

    for field in changed:
        setattr(lead, field, data[field])

    # Input is validated by the serializer before it reaches the service
    lead.save(update_fields=[*changed, "updated_at"])

    labels = [field.replace("_", " ") for field in changed]
    listed = labels[0] if len(labels) == 1 else f"{', '.join(labels[:-1])} and {labels[-1]}"

    LeadActivity.objects.create(
        lead=lead,
        user=performed_by,
        activity_type=ActivityType.UPDATED,
        description=f"{performed_by.get_full_name()} updated {listed}.",
    )

    return lead


@transaction.atomic
def add_lead_note(
    *,
    lead: Lead,
    content: str,
    author: User,
) -> LeadNote:
    """Create a note for a lead and record its creation activity."""

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
    """Change a lead's status and record the transition activity."""

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
            {
                "status": (
                    f"Cannot change status from {current_status.label} "
                    f"to {new_status.label}."
                )
            }
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
    """Assign a lead to a member and record the assignment activity."""

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
        description=(
            f"Lead assigned to {assigned_to.get_full_name()} "
            f"by {performed_by.get_full_name()}."
        ),
    )

    return lead


@transaction.atomic
def update_lead_note(
    *,
    note: LeadNote,
    content: str,
) -> LeadNote:
    """Update a lead note's content."""

    note.content = content

    note.save(
        update_fields=[
            "content",
            "updated_at",
        ],
    )

    return note


@transaction.atomic
def delete_lead_note(
    *,
    note: LeadNote,
) -> None:
    """Delete a lead note."""

    note.delete()
