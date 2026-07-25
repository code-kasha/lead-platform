# ==============================================================================
# Model Tests
# ==============================================================================

from apps.accounts.tests.factories import create_user
from django.test import TestCase


class UserModelTests(TestCase):
    """Verify user model behaviour."""

    def test_password_is_hashed(self):
        user = create_user()

        self.assertNotEqual(
            user.password,
            "password123",
        )

        self.assertTrue(user.check_password("password123"))

    def test_email_is_username_field(self):
        user = create_user()

        self.assertEqual(
            user.USERNAME_FIELD,
            "email",
        )

    def test_user_role_default(self):
        user = create_user()

        self.assertEqual(
            user.role,
            "MEMBER",
        )
