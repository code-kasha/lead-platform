from apps.accounts.permissions import IsAdmin
from apps.accounts.tests.factories import create_admin, create_user
from django.test import TestCase
from rest_framework.request import Request
from rest_framework.test import APIRequestFactory
from rest_framework.views import APIView


class DummyView(APIView):
    """Minimal view used for permission tests."""


class PermissionTests(TestCase):
    """Verify role-based permission behaviour."""

    factory: APIRequestFactory
    view: APIView

    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = DummyView()

    def test_admin_permission(self) -> None:
        user = create_admin()

        wsgi_request = self.factory.get("/")
        wsgi_request.user = user

        request = Request(wsgi_request)

        permission = IsAdmin()

        self.assertTrue(
            permission.has_permission(
                request,
                self.view,
            )
        )

    def test_member_cannot_access_admin_permission(self) -> None:
        user = create_user()

        wsgi_request = self.factory.get("/")
        wsgi_request.user = user

        request = Request(wsgi_request)

        permission = IsAdmin()

        self.assertFalse(
            permission.has_permission(
                request,
                self.view,
            )
        )
