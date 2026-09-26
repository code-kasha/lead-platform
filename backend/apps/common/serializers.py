# ==============================================================================
# Shared API Serializers
# ==============================================================================

from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    """Serialize standard human-readable API messages."""

    message = serializers.CharField(
        help_text="Human readable response message.",
    )


class ErrorSerializer(serializers.Serializer):
    """Serialize standard API error details."""

    detail = serializers.CharField(
        help_text="Error description.",
    )


class TokenSerializer(serializers.Serializer):
    """Serialize JWT access and refresh tokens."""

    access = serializers.CharField(
        help_text="JWT access token.",
    )

    refresh = serializers.CharField(
        help_text="JWT refresh token.",
    )


class LoginRequestSerializer(serializers.Serializer):
    """Validate credentials submitted for authentication."""

    email = serializers.EmailField(
        help_text="Registered email address.",
    )

    password = serializers.CharField(
        write_only=True,
        help_text="User password.",
    )
