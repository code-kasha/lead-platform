# ==============================================================================
# Lead Activity Serializer
# ==============================================================================

from apps.leads.models import LeadActivity
from rest_framework import serializers


class LeadActivitySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(help_text="The user who created the activity.", read_only=True)

    class Meta:
        model = LeadActivity
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_by",
            "created_at",
            "updated_at",
        )
