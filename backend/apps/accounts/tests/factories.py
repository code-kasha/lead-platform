# ==============================================================================
# Factories for the User tests
# ==============================================================================


from apps.accounts.choices import UserRole
from apps.accounts.models import User


def create_user(
    email="user@test.com",
    password="password123",
    role=UserRole.MEMBER,
):
    return User.objects.create_user(  # type: ignore
        email=email,
        password=password,
        first_name="Test",
        last_name="User",
        role=role,
    )


def create_admin(
    email="admin@test.com",
    password="password123",
):
    return User.objects.create_superuser(  # type: ignore
        email=email,
        password=password,
        first_name="Admin",
        last_name="User",
    )
