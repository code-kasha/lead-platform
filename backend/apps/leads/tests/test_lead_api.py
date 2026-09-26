# ==============================================================================
# Lead API Tests
# ==============================================================================

from typing import Any, cast
from unittest import mock

from apps.accounts.models import User
from apps.accounts.tests.factories import create_admin, create_user
from apps.leads.choices import ActivityType, LeadStatus
from apps.leads.models import Lead, LeadActivity
from apps.leads.tests.factories import create_lead
from django.core.cache import cache
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken

LEADS_URL = "/api/leads/"
PUBLIC_URL = "/api/leads/public/"

NEW_LEAD = {
    "first_name": "Ada",
    "last_name": "Lovelace",
    "email": "ada@example.com",
    "phone": "5550100",
    "company": "Engines Ltd",
    "source": "Referral",
}


class LeadApiTestCase(APITestCase):
    """Shared users and helpers for lead API tests."""

    client: APIClient

    def setUp(self) -> None:
        cache.clear()

        self.admin = create_admin()
        self.member = create_user(email="member@test.com")
        self.other = create_user(email="other@test.com")

    def authenticate(self, user: User) -> None:
        """Send requests as the given user."""

        token = RefreshToken.for_user(user).access_token
        cast(APIClient, self.client).credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def data(self, response: Any) -> Any:
        return cast(Response, response).data


# ==============================================================================
# Visibility
# ==============================================================================


class LeadVisibilityTests(LeadApiTestCase):
    """Members only see leads they created or are assigned to."""

    def setUp(self) -> None:
        super().setUp()

        self.created = create_lead(first_name="Created", created_by=self.member)
        self.assigned = create_lead(first_name="Assigned", created_by=self.admin, assigned_to=self.member)
        self.hidden = create_lead(first_name="Hidden", created_by=self.other)

    def names(self) -> set[str]:
        return {lead["first_name"] for lead in self.data(self.client.get(LEADS_URL))["results"]}

    def test_admin_sees_every_lead(self) -> None:
        self.authenticate(self.admin)

        self.assertEqual(self.names(), {"Created", "Assigned", "Hidden"})

    def test_member_sees_created_and_assigned_leads_only(self) -> None:
        self.authenticate(self.member)

        self.assertEqual(self.names(), {"Created", "Assigned"})

    def test_member_cannot_retrieve_another_members_lead(self) -> None:
        self.authenticate(self.member)

        response = self.client.get(f"{LEADS_URL}{self.hidden.pk}/")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_requests_are_rejected(self) -> None:
        response = self.client.get(LEADS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


# ==============================================================================
# Create, update, delete
# ==============================================================================


class LeadWriteTests(LeadApiTestCase):
    """Creating, editing and deleting leads, and the activity they record."""

    def test_create_sets_owner_and_new_status_and_records_activity(self) -> None:
        self.authenticate(self.member)

        response = self.client.post(LEADS_URL, NEW_LEAD, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lead = Lead.objects.get(pk=self.data(response)["id"])
        self.assertEqual(lead.created_by, self.member)
        self.assertEqual(lead.status, LeadStatus.NEW)
        self.assertIsNone(lead.assigned_to)

        activity = LeadActivity.objects.get(lead=lead)
        self.assertEqual(activity.activity_type, ActivityType.CREATED)
        self.assertEqual(activity.user, self.member)
        self.assertEqual(activity.description, "Lead created by Test User.")

    def test_create_rejects_a_phone_number_with_letters(self) -> None:
        self.authenticate(self.member)

        response = self.client.post(LEADS_URL, {**NEW_LEAD, "phone": "555-CALL"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("phone", self.data(response))
        self.assertFalse(Lead.objects.exists())

    def test_update_records_which_fields_changed(self) -> None:
        lead = create_lead(created_by=self.member, company="Old Co", source="Website")
        self.authenticate(self.member)

        response = self.client.patch(
            f"{LEADS_URL}{lead.pk}/",
            {"company": "New Co", "source": "Referral"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        lead.refresh_from_db()
        self.assertEqual((lead.company, lead.source), ("New Co", "Referral"))

        activity = LeadActivity.objects.get(lead=lead, activity_type=ActivityType.UPDATED)
        self.assertEqual(activity.user, self.member)
        self.assertEqual(activity.description, "Test User updated company and source.")

    def test_update_without_changes_records_nothing(self) -> None:
        lead = create_lead(created_by=self.member, company="Same Co")
        self.authenticate(self.member)

        response = self.client.patch(f"{LEADS_URL}{lead.pk}/", {"company": "Same Co"}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(LeadActivity.objects.filter(lead=lead, activity_type=ActivityType.UPDATED).exists())

    def test_update_cannot_change_status_or_owner(self) -> None:
        lead = create_lead(created_by=self.member)
        self.authenticate(self.member)

        self.client.patch(
            f"{LEADS_URL}{lead.pk}/",
            {"status": LeadStatus.WON, "created_by": self.other.pk, "assigned_to": self.other.pk},
            format="json",
        )

        lead.refresh_from_db()
        self.assertEqual(lead.status, LeadStatus.NEW)
        self.assertEqual(lead.created_by, self.member)
        self.assertIsNone(lead.assigned_to)

    def test_assignee_can_edit_but_not_delete(self) -> None:
        lead = create_lead(created_by=self.admin, assigned_to=self.member)
        self.authenticate(self.member)

        edit = self.client.patch(f"{LEADS_URL}{lead.pk}/", {"company": "Edited"}, format="json")
        delete = self.client.delete(f"{LEADS_URL}{lead.pk}/")

        self.assertEqual(edit.status_code, status.HTTP_200_OK)
        self.assertEqual(delete.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Lead.objects.filter(pk=lead.pk).exists())

    def test_admin_can_delete(self) -> None:
        lead = create_lead(created_by=self.member)
        self.authenticate(self.admin)

        response = self.client.delete(f"{LEADS_URL}{lead.pk}/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lead.objects.filter(pk=lead.pk).exists())


# ==============================================================================
# Filtering, search, ordering, pagination
# ==============================================================================


class LeadQueryTests(LeadApiTestCase):
    """Query parameters on the lead list."""

    def setUp(self) -> None:
        super().setUp()
        self.authenticate(self.admin)

        create_lead(first_name="Carol", company="Umbrella", status=LeadStatus.NEW, created_by=self.admin)
        create_lead(first_name="Alice", company="Acme", status=LeadStatus.QUALIFIED, created_by=self.admin)
        create_lead(
            first_name="Bob",
            company="Acme",
            status=LeadStatus.NEW,
            created_by=self.admin,
            assigned_to=self.member,
        )

    def names(self, query: str) -> list[str]:
        return [lead["first_name"] for lead in self.data(self.client.get(f"{LEADS_URL}?{query}"))["results"]]

    def test_filter_by_status(self) -> None:
        self.assertEqual(sorted(self.names("status=NEW")), ["Bob", "Carol"])

    def test_filter_by_assignee(self) -> None:
        self.assertEqual(self.names(f"assigned_to={self.member.pk}"), ["Bob"])

    def test_search_across_name_email_phone_and_company(self) -> None:
        self.assertEqual(sorted(self.names("search=acme")), ["Alice", "Bob"])

    def test_ordering(self) -> None:
        self.assertEqual(self.names("ordering=first_name"), ["Alice", "Bob", "Carol"])
        self.assertEqual(self.names("ordering=-first_name"), ["Carol", "Bob", "Alice"])

    def test_pagination_envelope_and_page_size(self) -> None:
        body = self.data(self.client.get(f"{LEADS_URL}?page_size=2&ordering=first_name"))

        self.assertEqual(body["count"], 3)
        self.assertEqual([lead["first_name"] for lead in body["results"]], ["Alice", "Bob"])
        self.assertIsNotNone(body["next"])


# ==============================================================================
# Public form
# ==============================================================================


class PublicLeadTests(LeadApiTestCase):
    """The unauthenticated lead form."""

    def test_anonymous_visitor_can_submit_a_lead(self) -> None:
        response = self.client.post(PUBLIC_URL, NEW_LEAD, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        lead = Lead.objects.get(pk=self.data(response)["id"])
        self.assertIsNone(lead.created_by)
        self.assertEqual(lead.status, LeadStatus.NEW)

        activity = LeadActivity.objects.get(lead=lead)
        self.assertEqual(activity.activity_type, ActivityType.CREATED)
        self.assertIsNone(activity.user)
        self.assertEqual(activity.description, "Lead submitted through the public form.")

    def test_public_submissions_are_rate_limited(self) -> None:
        with mock.patch.dict(ScopedRateThrottle.THROTTLE_RATES, {"public_leads": "2/hour"}):
            codes = [
                self.client.post(PUBLIC_URL, {**NEW_LEAD, "email": f"lead{i}@example.com"}, format="json").status_code
                for i in range(3)
            ]

        self.assertEqual(codes, [201, 201, 429])
        self.assertEqual(Lead.objects.count(), 2)

    def test_signed_in_endpoints_are_not_rate_limited_by_the_public_scope(self) -> None:
        self.authenticate(self.member)

        with mock.patch.dict(ScopedRateThrottle.THROTTLE_RATES, {"public_leads": "1/hour"}):
            codes = [
                self.client.post(LEADS_URL, {**NEW_LEAD, "email": f"lead{i}@example.com"}, format="json").status_code
                for i in range(3)
            ]

        self.assertEqual(codes, [201, 201, 201])
