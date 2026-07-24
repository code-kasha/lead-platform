# ==============================================================================
# Lead Serializers
# ==============================================================================

from apps.accounts.models import User
from apps.accounts.serializers import UserSummarySerializer
from apps.leads.models import Lead
from rest_framework import serializers


class LeadSerializer(serializers.ModelSerializer):
    created_by = UserSummarySerializer(read_only=True)
    assigned_to = UserSummarySerializer(read_only=True)

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
            "created_by",
            "created_at",
            "updated_at",
        )


class LeadCreateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Lead
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "source",
            "status",
            "assigned_to",
        )


class LeadUpdateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Lead
        fields = (
            "first_name",
            "last_name",
            "email",
            "phone",
            "company",
            "source",
            "status",
            "assigned_to",
        )
