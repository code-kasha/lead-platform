# ==============================================================================
# Authentication tests
# ==============================================================================

from typing import Any, cast

from apps.accounts.tests.factories import create_user
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase


class AuthenticationTests(APITestCase):
    client = APIClient()
    login_url = "/api/auth/login/"
    refresh_url = "/api/auth/refresh/"
    me_url = "/api/auth/me/"

    def setUp(self):
        self.user = create_user()

    def test_login_returns_tokens(self):

        response = cast(
            Response,
            self.client.post(
                self.login_url,
                {
                    "email": "user@test.com",
                    "password": "password123",
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

        self.assertIn(
            "access",
            data,
        )

        self.assertIn(
            "refresh",
            data,
        )

    def test_refresh_returns_new_access_token(self):

        login = cast(
            Response,
            self.client.post(
                self.login_url,
                {
                    "email": "user@test.com",
                    "password": "password123",
                },
                format="json",
            ),
        )

        login_data = cast(
            dict[str, Any],
            login.data,
        )

        refresh_token = login_data["refresh"]

        response = cast(
            Response,
            self.client.post(
                self.refresh_url,
                {
                    "refresh": refresh_token,
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

        self.assertIn(
            "access",
            data,
        )

    def test_me_requires_authentication(self):

        response = cast(
            Response,
            self.client.get(
                self.me_url,
            ),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


def test_authenticated_user_can_access_me(self):

    login = cast(
        Response,
        self.client.post(
            self.login_url,
            {
                "email": "user@test.com",
                "password": "password123",
            },
            format="json",
        ),
    )

    login_data = cast(
        dict[str, Any],
        login.data,
    )

    token = login_data["access"]

    client = cast(
        APIClient,
        self.client,
    )

    client.credentials(
        HTTP_AUTHORIZATION=f"Bearer {token}",
    )

    response = cast(
        Response,
        client.get(
            self.me_url,
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

    self.assertEqual(
        data["email"],
        "user@test.com",
    )
