# ==============================================================================
# Note API Tests
# ==============================================================================

from typing import Any, cast

from apps.accounts.tests.factories import create_admin, create_user
from apps.leads.choices import ActivityType
from apps.leads.models import LeadActivity, LeadNote
from apps.leads.tests.factories import create_lead
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class AddLeadNoteTests(APITestCase):
    client: APIClient

    def setUp(self):
        self.admin = create_admin()
        self.member = create_user(email="member@test.com")
        self.other = create_user(email="other@test.com")

        self.lead = create_lead(
            created_by=self.admin,
            assigned_to=self.member,
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

    def test_admin_can_add_note(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/notes/",
                {
                    "content": "Called customer.",
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
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            data["content"],
            "Called customer.",
        )

        self.assertTrue(
            LeadNote.objects.filter(
                lead=self.lead,
                content="Called customer.",
            ).exists()
        )

    def test_assigned_member_can_add_note(self):
        self.authenticate(self.member)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/notes/",
                {
                    "content": "Follow-up scheduled.",
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
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
                f"/api/leads/{self.lead.pk}/notes/",
                {
                    "content": "Should fail.",
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_note_creates_activity(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/notes/",
                {
                    "content": "Customer interested.",
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertTrue(
            LeadActivity.objects.filter(
                lead=self.lead,
                activity_type=ActivityType.NOTE_ADDED,
            ).exists()
        )

    def test_empty_note_returns_bad_request(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.post(
                f"/api/leads/{self.lead.pk}/notes/",
                {
                    "content": "",
                },
                format="json",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
