# ==============================================================================
# Lead Note Update API Tests
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


class UpdateLeadNoteTests(APITestCase):
    """Verify lead note update endpoint behaviour."""
    client: APIClient

    def setUp(self):
        self.admin = create_admin()
        self.member = create_user(email="member@test.com")

        self.lead = create_lead(
            created_by=self.admin,
            assigned_to=self.member,
        )

        self.note = LeadNote.objects.create(
            lead=self.lead,
            author=self.member,
            content="Original note",
        )

    def authenticate(
        self,
        user: User,
    ):
        refresh = RefreshToken.for_user(user)

        client = cast(
            APIClient,
            self.client,
        )

        client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}",
        )

    def test_admin_can_update_note(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.patch(
                f"/api/leads/notes/{self.note.pk}/",
                {
                    "content": "Updated note",
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

        self.note.refresh_from_db()

        self.assertEqual(
            self.note.content,
            "Updated note",
        )

        self.assertEqual(
            data["content"],
            "Updated note",
        )

    def test_author_can_update_note(self):
        self.authenticate(self.member)
        client = cast(
            APIClient,
            self.client,
        )
        response = cast(
            Response,
            client.patch(
                f"/api/leads/notes/{self.note.pk}/",
                {
                    "content": "Author updated note",
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
        self.note.refresh_from_db()
        self.assertEqual(
            self.note.content,
            "Author updated note",
        )
        self.assertEqual(
            data["content"],
            "Author updated note",
        )

    def test_non_author_receives_not_found(self):
        other = create_user(
            email="other@test.com",
        )
        self.authenticate(other)
        client = cast(
            APIClient,
            self.client,
        )
        response = cast(
            Response,
            client.patch(
                f"/api/leads/notes/{self.note.pk}/",
                {
                    "content": "Should fail",
                },
                format="json",
            ),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_empty_content_returns_bad_request(self):
        self.authenticate(self.admin)
        client = cast(
            APIClient,
            self.client,
        )
        response = cast(
            Response,
            client.patch(
                f"/api/leads/notes/{self.note.pk}/",
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

    def test_updated_at_changes(self):
        self.authenticate(self.admin)
        original_updated_at = self.note.updated_at
        client = cast(
            APIClient,
            self.client,
        )
        response = cast(
            Response,
            client.patch(
                f"/api/leads/notes/{self.note.pk}/",
                {
                    "content": "Timestamp updated",
                },
                format="json",
            ),
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.note.refresh_from_db()
        self.assertGreater(
            self.note.updated_at,
            original_updated_at,
        )
