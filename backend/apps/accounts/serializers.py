# ==============================================================================
# Serializer for the User model
# ==============================================================================

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "User",
            value={
                "id": 1,
                "email": "admin@example.com",
                "first_name": "Akash",
                "last_name": "Damle",
                "role": "ADMIN",
            },
        )
    ]
)
class UserSerializer(serializers.ModelSerializer):
    """Serialize read-only user account details."""

    id = serializers.IntegerField(
        read_only=True,
        help_text="Unique user identifier.",
    )

    email = serializers.EmailField(
        read_only=True,
        help_text="Registered email address.",
    )

    first_name = serializers.CharField(
        read_only=True,
        help_text="User's first name.",
    )

    last_name = serializers.CharField(
        read_only=True,
        help_text="User's last name.",
    )

    role = serializers.CharField(
        read_only=True,
        help_text="Assigned user role.",
    )

    class Meta:
        model = User

        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "role",
        )

        read_only_fields = fields


class LoginSerializer(TokenObtainPairSerializer):
    """Add user details to issued JWT tokens."""

    @classmethod
    def get_token(cls, user):
        """Create a token containing the user's email and role."""

        token = super().get_token(user)

        token["email"] = user.email
        token["role"] = user.role

        return token


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            "User Summary",
            value={
                "id": 1,
                "full_name": "Akash Damle",
            },
        )
    ]
)
class UserSummarySerializer(serializers.ModelSerializer):
    """Serialize a lightweight representation of a user."""

    full_name = serializers.CharField(
        read_only=True,
        help_text="User's full name.",
    )

    class Meta:
        model = User

        fields = (
            "id",
            "full_name",
        )

        read_only_fields = fields


class LogoutSerializer(serializers.Serializer):
    """Validate a refresh token for invalidation."""

    refresh = serializers.CharField(
        help_text="Refresh token to invalidate.",
    )

    def validate(self, attrs):
        """Store the validated refresh token for invalidation."""

        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        """Blacklist the validated refresh token."""

        RefreshToken(self.token).blacklist()
