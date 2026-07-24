# ==============================================================================
# Factories for the Lead application
# ==============================================================================

import uuid

from apps.accounts.tests.factories import create_user
from apps.leads.choices import ActivityType, LeadStatus
from apps.leads.models import Lead, LeadActivity, LeadNote


def create_lead(
    first_name="John",
    last_name="Doe",
    email=None,
    phone="+919876543210",
    company="Acme Inc.",
    source="Website",
    status=LeadStatus.NEW,
    created_by=None,
    assigned_to=None,
):
    if email is None:
        email = f"{uuid.uuid4()}@test.com"

    if created_by is None:
        created_by = create_user(
            email=f"{uuid.uuid4()}@test.com",
        )

    return Lead.objects.create(
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone=phone,
        company=company,
        source=source,
        status=status,
        created_by=created_by,
        assigned_to=assigned_to,
    )


def create_note(
    lead=None,
    author=None,
    content="Test note",
):
    if lead is None:
        lead = create_lead()

    if author is None:
        author = create_user(
            email=f"{uuid.uuid4()}@test.com",
        )

    return LeadNote.objects.create(
        lead=lead,
        author=author,
        content=content,
    )


def create_activity(
    lead=None,
    user=None,
    activity_type=ActivityType.CREATED,
    description="Lead created",
):
    if lead is None:
        lead = create_lead()

    if user is None:
        user = create_user(
            email=f"{uuid.uuid4()}@test.com",
        )

    return LeadActivity.objects.create(
        lead=lead,
        user=user,
        activity_type=activity_type,
        description=description,
    )
