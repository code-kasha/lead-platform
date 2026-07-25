# ==============================================================================
# Lead Note List API Tests
# ==============================================================================

from typing import Any, cast

from apps.accounts.models import User
from apps.accounts.tests.factories import create_admin, create_user
from apps.leads.models import LeadNote
from apps.leads.tests.factories import create_lead
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class ListLeadNotesTests(APITestCase):
    """Verify lead note listing endpoint behaviour."""
    client: APIClient

    def setUp(self):
        self.admin = create_admin()
        self.member = create_user(email="member@test.com")
        self.other = create_user(email="other@test.com")

        self.lead = create_lead(
            created_by=self.admin,
            assigned_to=self.member,
        )

        LeadNote.objects.create(
            lead=self.lead,
            author=self.admin,
            content="First note",
        )

        LeadNote.objects.create(
            lead=self.lead,
            author=self.member,
            content="Second note",
        )

    def authenticate(self, user: User):
        refresh = RefreshToken.for_user(user)

        client = cast(
            APIClient,
            self.client,
        )

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
        )

    def test_admin_can_list_notes(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.get(
                f"/api/leads/{self.lead.pk}/notes/list/",
            ),
        )

        data = cast(
            list[dict[str, Any]],
            response.data,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(data),
            2,
        )

    def test_assigned_member_can_list_notes(self):
        self.authenticate(self.member)
        client = cast(
            APIClient,
            self.client,
        )
        response = cast(
            Response,
            client.get(
                f"/api/leads/{self.lead.pk}/notes/list/",
            ),
        )
        data = cast(
            list[dict[str, Any]],
            response.data,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            len(data),
            2,
        )

    def test_unrelated_member_receives_not_found(self):
        self.authenticate(self.other)
        client = cast(
            APIClient,
            self.client,
        )
        response = cast(
            Response,
            client.get(
                f"/api/leads/{self.lead.pk}/notes/list/",
            ),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_empty_notes_returns_empty_list(self):
        empty_lead = create_lead(
            created_by=self.admin,
            assigned_to=self.member,
        )
        self.authenticate(self.admin)
        client = cast(
            APIClient,
            self.client,
        )
        response = cast(
            Response,
            client.get(
                f"/api/leads/{empty_lead.pk}/notes/list/",
            ),
        )
        data = cast(
            list[dict[str, Any]],
            response.data,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data,
            [],
        )

    def test_notes_are_returned_newest_first(self):
        self.authenticate(self.admin)
        client = cast(
            APIClient,
            self.client,
        )
        response = cast(
            Response,
            client.get(
                f"/api/leads/{self.lead.pk}/notes/list/",
            ),
        )
        data = cast(
            list[dict[str, Any]],
            response.data,
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(
            data[0]["content"],
            "Second note",
        )
        self.assertEqual(
            data[1]["content"],
            "First note",
        )
