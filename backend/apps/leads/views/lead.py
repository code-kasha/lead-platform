# ==============================================================================
# Lead API Views
# ==============================================================================

from apps.leads.filters import LeadFilter
from apps.leads.models import Lead
from apps.leads.permissions import LeadPermission
from apps.leads.serializers import LeadCreateSerializer, LeadSerializer, LeadUpdateSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import ModelViewSet


class LeadViewSet(ModelViewSet):
    permission_classes = [LeadPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = LeadFilter

    search_fields = [
        "first_name",
        "last_name",
        "email",
        "company",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "first_name",
        "last_name",
    ]

    ordering = ["-created_at"]

    def get_queryset(self):
        return Lead.objects.select_related(
            "created_by",
            "assigned_to",
        ).order_by("-created_at")

    def get_serializer_class(self):
        if self.action == "create":
            return LeadCreateSerializer

        if self.action in ("update", "partial_update"):
            return LeadUpdateSerializer

        return LeadSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
