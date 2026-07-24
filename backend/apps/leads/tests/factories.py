# ==============================================================================
# Factories for the Lead tests
# ==============================================================================

import uuid

from apps.accounts.tests.factories import create_user
from apps.leads.choices import LeadStatus
from apps.leads.models import Lead


def create_lead(
    first_name="John",
    last_name="Doe",
    email="john.doe@test.com",
    phone="+919876543210",
    company="Acme Inc.",
    source="Website",
    status=LeadStatus.NEW,
    created_by=None,
    assigned_to=None,
):
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
