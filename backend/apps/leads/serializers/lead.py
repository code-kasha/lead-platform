# ==============================================================================
# Lead Serializers
# ==============================================================================

from apps.accounts.serializers import UserSummarySerializer
from apps.leads.models import Lead
from rest_framework import serializers


class LeadSerializer(serializers.ModelSerializer):
    """
    Serializer used for retrieving leads.
    """

    created_by = UserSummarySerializer(
        read_only=True,
        help_text="The user who created the lead.",
    )

    assigned_to = UserSummarySerializer(
        read_only=True,
        help_text="The user currently assigned to the lead.",
    )

    class Meta:
        model = Lead
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "source",
            "status",
            "created_by",
            "assigned_to",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "status",
            "created_by",
            "assigned_to",
            "created_at",
            "updated_at",
        )


class LeadCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used when creating a new lead.

    Status is automatically set to NEW.
    Assignment is handled through the dedicated assignment endpoint.
    """

    class Meta:
        model = Lead
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "source",
        )


class LeadUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer used for updating lead information.

    Assignment and status changes are handled through dedicated endpoints.
    """

    class Meta:
        model = Lead
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "source",
        )
