# ==============================================================================
# Model Tests
# ==============================================================================


from apps.accounts.tests.factories import create_user
from apps.leads.choices import LeadStatus
from apps.leads.tests.factories import create_lead
from django.test import TestCase


class LeadModelTests(TestCase):

    def test_create_lead(self):
        lead = create_lead()

        self.assertEqual(
            lead.first_name,
            "John",
        )

        self.assertEqual(
            lead.email,
            "john.doe@test.com",
        )

    def test_default_status_is_new(self):
        lead = create_lead()

        self.assertEqual(
            lead.status,
            LeadStatus.NEW,
        )

    def test_assign_lead_to_member(self):
        member = create_user(
            email="member@test.com",
        )

        lead = create_lead(
            assigned_to=member,
        )

        self.assertEqual(
            lead.assigned_to,
            member,
        )

    def test_created_by_is_saved(self):
        creator = create_user(
            email="creator@test.com",
        )

        lead = create_lead(
            created_by=creator,
        )

        self.assertEqual(
            lead.created_by,
            creator,
        )

    def test_string_representation(self):
        lead = create_lead()

        self.assertEqual(
            str(lead),
            "John Doe",
        )

    def test_ordering(self):
        create_lead(
            email="first@test.com",
        )

        newest = create_lead(
            email="second@test.com",
        )

        first = newest.__class__.objects.first()

        self.assertEqual(
            first.email,
            "second@test.com",
        )
