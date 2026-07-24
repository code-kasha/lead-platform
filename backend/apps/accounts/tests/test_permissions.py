# ==============================================================================
# Permission tests
# ==============================================================================

from apps.accounts.permissions import IsAdmin, IsMember
from apps.accounts.tests.factories import create_admin, create_user
from django.test import TestCase
from rest_framework.test import APIRequestFactory


class PermissionTests(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()

    def test_admin_permission(self):

        user = create_admin()

        request = self.factory.get("/")

        request.user = user

        permission = IsAdmin()

        self.assertTrue(
            permission.has_permission(
                request,
                None,
            )
        )

    def test_member_cannot_access_admin_permission(self):

        user = create_user()

        request = self.factory.get("/")

        request.user = user

        permission = IsAdmin()

        self.assertFalse(
            permission.has_permission(
                request,
                None,
            )
        )
