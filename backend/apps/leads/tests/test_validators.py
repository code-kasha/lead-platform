# ==============================================================================
# Validator Tests
# ==============================================================================

from apps.accounts.tests.factories import create_user
from apps.leads.models import Lead
from django.core.exceptions import ValidationError
from django.test import TestCase


class LeadValidatorTests(TestCase):
    """Verify lead validation behaviour."""

    def test_valid_phone(self):

        lead = Lead(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="+919876543210",
            created_by=create_user(),
        )

        # Should not raise
        lead.full_clean()

    def test_invalid_phone(self):

        lead = Lead(
            first_name="John",
            last_name="Doe",
            email="john@test.com",
            phone="abc123",
            created_by=create_user(),
        )

        with self.assertRaises(ValidationError):
            lead.full_clean()
