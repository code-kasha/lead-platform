# ==============================================================================
# Activity Model Tests
# ==============================================================================

from apps.leads.choices import ActivityType
from apps.leads.tests.factories import create_activity
from django.test import TestCase


class LeadActivityModelTests(TestCase):
    """Verify lead activity model behaviour."""

    def test_create_activity(self):
        activity = create_activity()

        self.assertEqual(
            activity.activity_type,
            ActivityType.CREATED,
        )

    def test_activity_has_description(self):
        activity = create_activity()

        self.assertEqual(
            activity.description,
            "Lead created",
        )

    def test_activity_string_representation(self):
        activity = create_activity()

        self.assertIn(
            "CREATED",
            str(activity),
        )

    def test_activity_ordering(self):
        create_activity(
            description="Old",
        )

        newest = create_activity(
            description="New",
        )

        self.assertEqual(
            newest.__class__.objects.first(),
            newest,
        )
