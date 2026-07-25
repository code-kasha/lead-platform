# ==============================================================================
# Lead Note Delete API Tests
# ==============================================================================

from typing import cast

from apps.accounts.models import User
from apps.accounts.tests.factories import create_admin, create_user
from apps.leads.models import LeadNote
from apps.leads.tests.factories import create_lead
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class DeleteLeadNoteTests(APITestCase):
    """Verify lead note deletion endpoint behaviour."""
    client: APIClient

    def setUp(self):
        self.admin = create_admin()
        self.member = create_user(
            email="member@test.com",
        )
        self.other = create_user(
            email="other@test.com",
        )

        self.lead = create_lead(
            created_by=self.admin,
            assigned_to=self.member,
        )

        self.note = LeadNote.objects.create(
            lead=self.lead,
            author=self.member,
            content="Delete me",
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

    def test_admin_can_delete_note(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.delete(
                f"/api/leads/notes/{self.note.pk}/",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            LeadNote.objects.filter(
                pk=self.note.pk,
            ).exists(),
        )

    def test_author_can_delete_note(self):
        self.authenticate(self.member)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.delete(
                f"/api/leads/notes/{self.note.pk}/",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            LeadNote.objects.filter(
                pk=self.note.pk,
            ).exists(),
        )

    def test_non_author_receives_not_found(self):
        self.authenticate(self.other)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.delete(
                f"/api/leads/notes/{self.note.pk}/",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            LeadNote.objects.filter(
                pk=self.note.pk,
            ).exists(),
        )

    def test_deleted_note_no_longer_exists(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.delete(
                f"/api/leads/notes/{self.note.pk}/",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertEqual(
            LeadNote.objects.count(),
            0,
        )
