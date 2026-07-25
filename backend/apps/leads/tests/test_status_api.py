# ==============================================================================
# Status API Tests
# ==============================================================================

from typing import Any, cast

from apps.accounts.tests.factories import create_admin, create_user
from apps.leads.choices import ActivityType, LeadStatus
from apps.leads.models import LeadActivity
from apps.leads.tests.factories import create_lead
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class ChangeLeadStatusTests(APITestCase):
    """Verify lead status change endpoint behaviour."""
    client: APIClient

    def setUp(self):
        self.admin = create_admin()
        self.member = create_user(email="member@test.com")
        self.other = create_user(email="other@test.com")

        self.lead = create_lead(
            created_by=self.admin,
            assigned_to=self.member,
            status=LeadStatus.NEW,
        )

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)

        client = cast(
            APIClient,
            self.client,
        )

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
        )

    def test_admin_can_change_status(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/status/",
                {
                    "status": LeadStatus.CONTACTED,
                },
                format="json",
            ),
        )

        data = cast(
            dict[str, Any],
            response.data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIsNotNone(data)

        self.lead.refresh_from_db()

        self.assertEqual(
            self.lead.status,
            LeadStatus.CONTACTED,
        )

    def test_assigned_member_can_change_status(self):
        self.authenticate(self.member)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/status/",
                {
                    "status": LeadStatus.CONTACTED,
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.lead.refresh_from_db()

        self.assertEqual(
            self.lead.status,
            LeadStatus.CONTACTED,
        )

    def test_unrelated_member_receives_not_found(self):
        self.authenticate(self.other)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/status/",
                {
                    "status": LeadStatus.CONTACTED,
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.lead.refresh_from_db()

        self.assertEqual(
            self.lead.status,
            LeadStatus.NEW,
        )

        self.assertFalse(
            LeadActivity.objects.filter(
                lead=self.lead,
                activity_type=ActivityType.STATUS_CHANGED,
            ).exists()
        )

    def test_status_change_creates_activity(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/status/",
                {
                    "status": LeadStatus.CONTACTED,
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertTrue(
            LeadActivity.objects.filter(
                lead=self.lead,
                activity_type=ActivityType.STATUS_CHANGED,
            ).exists()
        )

    def test_invalid_status_returns_bad_request(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/status/",
                {
                    "status": "INVALID_STATUS",
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_cannot_change_to_same_status(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/status/",
                {
                    "status": LeadStatus.NEW,
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_invalid_status_transition_returns_bad_request(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/status/",
                {
                    "status": LeadStatus.WON,
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.lead.refresh_from_db()

        self.assertEqual(
            self.lead.status,
            LeadStatus.NEW,
        )
