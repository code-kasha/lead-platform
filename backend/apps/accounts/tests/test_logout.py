from apps.accounts.tests.factories import create_user
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutTests(APITestCase):

    def setUp(self):
        self.user = create_user()

        refresh = RefreshToken.for_user(self.user)

        self.refresh = str(refresh)
        self.access = str(refresh.access_token)

        self.client.credentials(  # type: ignore
            HTTP_AUTHORIZATION=f"Bearer {self.access}",
        )

    def test_logout_success(self):
        response = self.client.post(
            "/api/auth/logout/",
            {
                "refresh": self.refresh,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_205_RESET_CONTENT,
        )

    def test_logout_requires_authentication(self):
        self.client.credentials()  # type: ignore

        response = self.client.post(
            "/api/auth/logout/",
            {
                "refresh": self.refresh,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
