# ==============================================================================
# Shared API Serializers
# ==============================================================================

from rest_framework import serializers


class MessageSerializer(serializers.Serializer):
    message = serializers.CharField(
        help_text="Human readable response message.",
    )


class ErrorSerializer(serializers.Serializer):
    detail = serializers.CharField(
        help_text="Error description.",
    )


class TokenSerializer(serializers.Serializer):
    access = serializers.CharField(
        help_text="JWT access token.",
    )

    refresh = serializers.CharField(
        help_text="JWT refresh token.",
    )


class AccessTokenSerializer(serializers.Serializer):
    access = serializers.CharField(
        help_text="New JWT access token.",
    )


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(
        help_text="Registered email address.",
    )

    password = serializers.CharField(
        write_only=True,
        help_text="User password.",
    )
