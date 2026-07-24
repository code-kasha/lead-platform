# ==============================================================================
# Lead Note Serializer
# ==============================================================================

from apps.leads.models import LeadNote
from rest_framework import serializers


class LeadNoteSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = LeadNote
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_by",
            "created_at",
            "updated_at",
        )
