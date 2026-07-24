# ==============================================================================
# Lead Note Serializers
# ==============================================================================

from apps.accounts.serializers import UserSummarySerializer
from apps.leads.models import LeadNote
from rest_framework import serializers


class LeadNoteSerializer(serializers.ModelSerializer):
    """
    Serializer used for retrieving lead notes.
    """

    author = UserSummarySerializer(
        read_only=True,
        help_text="The user who created the note.",
    )

    class Meta:
        model = LeadNote

        fields = (
            "id",
            "lead",
            "content",
            "author",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "author",
            "created_at",
            "updated_at",
        )


class LeadNoteCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used when creating a lead note.
    """

    class Meta:
        model = LeadNote

        fields = ("content",)


class LeadNoteUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer used when updating a lead note.
    """

    class Meta:
        model = LeadNote

        fields = ("content",)
