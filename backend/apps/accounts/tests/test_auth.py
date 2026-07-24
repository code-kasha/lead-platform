# ==============================================================================
# Authentication tests
# ==============================================================================

from rest_framework.test import APITestCase
from rest_framework import status

from apps.accounts.tests.factories import create_user


class AuthenticationTests(APITestCase):

    login_url = "/api/auth/login/"
    refresh_url = "/api/auth/refresh/"
    me_url = "/api/auth/me/"

    def setUp(self):
        self.user = create_user()

    def test_login_returns_tokens(self):

        response = self.client.post(
            self.login_url,
            {
                "email": "user@test.com",
                "password": "password123",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

        self.assertIn(
            "refresh",
            response.data,
        )

    def test_refresh_returns_new_access_token(self):

        login = self.client.post(
            self.login_url,
            {
                "email": "user@test.com",
                "password": "password123",
            },
            format="json",
        )

        refresh_token = login.data["refresh"]

        response = self.client.post(
            self.refresh_url,
            {
                "refresh": refresh_token,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertIn(
            "access",
            response.data,
        )

    def test_me_requires_authentication(self):

        response = self.client.get(
            self.me_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    def test_authenticated_user_can_access_me(self):

        login = self.client.post(
            self.login_url,
            {
                "email": "user@test.com",
                "password": "password123",
            },
            format="json",
        )

        token = login.data["access"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

        response = self.client.get(
            self.me_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["email"],
            "user@test.com",
        )
