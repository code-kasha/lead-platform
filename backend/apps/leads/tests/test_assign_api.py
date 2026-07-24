# ==============================================================================
# Assignment API Tests
# ==============================================================================

from typing import Any, cast

from apps.accounts.tests.factories import create_admin, create_user
from apps.leads.choices import ActivityType
from apps.leads.models import LeadActivity
from apps.leads.tests.factories import create_lead
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class AssignLeadTests(APITestCase):
    client: APIClient

    def setUp(self):
        self.admin = create_admin()
        self.member = create_user(email="member@test.com")
        self.lead = create_lead(created_by=self.admin)

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)

        client = cast(
            APIClient,
            self.client,
        )

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
        )

    def test_admin_can_assign_lead(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/assign/",
                {
                    "assigned_to": self.member.pk,
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
            self.lead.assigned_to,
            self.member,
        )

    def test_member_cannot_assign_lead(self):
        self.authenticate(self.member)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/assign/",
                {
                    "assigned_to": self.member.pk,
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    def test_assignment_creates_activity(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/assign/",
                {
                    "assigned_to": self.member.pk,
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
                activity_type=ActivityType.ASSIGNED,
            ).exists()
        )

    def test_invalid_member_returns_bad_request(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/assign/",
                {
                    "assigned_to": 999999,
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
