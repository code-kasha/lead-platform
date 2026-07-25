# ==============================================================================
# Lead Activity API Tests
# ==============================================================================

from typing import Any, cast

from apps.accounts.models import User
from apps.accounts.tests.factories import create_admin, create_user
from apps.leads.choices import ActivityType
from apps.leads.models import LeadActivity
from apps.leads.tests.factories import create_lead
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class ListLeadActivityTests(APITestCase):
    """Verify lead activity listing behaviour."""
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

        self.first_activity = LeadActivity.objects.create(
            lead=self.lead,
            user=self.admin,
            activity_type=ActivityType.CREATED,
            description="Lead created.",
        )

        self.second_activity = LeadActivity.objects.create(
            lead=self.lead,
            user=self.member,
            activity_type=ActivityType.NOTE_ADDED,
            description="Added note.",
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

    def test_admin_can_list_activities(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.get(
                f"/api/leads/{self.lead.pk}/activities/",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        data = cast(
            list[dict[str, Any]],
            response.data,
        )

        self.assertEqual(
            len(data),
            2,
        )

    def test_assigned_member_can_list_activities(self):
        self.authenticate(self.member)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.get(
                f"/api/leads/{self.lead.pk}/activities/",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
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
                f"/api/leads/{self.lead.pk}/activities/",
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_returns_all_activities(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.get(
                f"/api/leads/{self.lead.pk}/activities/",
            ),
        )

        data = cast(
            list[dict[str, Any]],
            response.data,
        )

        self.assertEqual(
            len(data),
            LeadActivity.objects.filter(
                lead=self.lead,
            ).count(),
        )

    def test_activities_are_returned_newest_first(self):
        self.authenticate(self.admin)

        client = cast(
            APIClient,
            self.client,
        )

        response = cast(
            Response,
            client.get(
                f"/api/leads/{self.lead.pk}/activities/",
            ),
        )

        data = cast(
            list[dict[str, Any]],
            response.data,
        )

        self.assertEqual(
            data[0]["id"],
            self.second_activity.pk,
        )

        self.assertEqual(
            data[1]["id"],
            self.first_activity.pk,
        )
