# ==============================================================================
# Serializer for the User model
# ==============================================================================

from drf_spectacular.utils import OpenApiExample, extend_schema_serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

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

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["role"] = user.role

        return token


class UserSummarySerializer(UserSerializer):
    pass
