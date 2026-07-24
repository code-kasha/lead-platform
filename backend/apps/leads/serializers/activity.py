# ==============================================================================
# Lead Activity Serializer
# ==============================================================================

from apps.leads.models import LeadActivity
from rest_framework import serializers


class LeadActivitySerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField()

    class Meta:
        model = LeadActivity
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_by",
            "created_at",
            "updated_at",
        )
