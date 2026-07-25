# ==============================================================================
# Lead Activity Serializers
# ==============================================================================

from apps.accounts.serializers import UserSummarySerializer
from apps.leads.models import LeadActivity
from rest_framework import serializers


class LeadActivitySerializer(serializers.ModelSerializer):
    """
    Serializer used for retrieving lead activities.
    """

    user = UserSummarySerializer(
        read_only=True,
        help_text="The user who performed the activity.",
    )

    class Meta:
        model = LeadActivity

        fields = "__all__"

        read_only_fields = (
            "id",
            "lead",
            "user",
            "activity_type",
            "description",
            "created_at",
            "updated_at",
        )
