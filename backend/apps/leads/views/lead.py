# ==============================================================================
# Lead API Views
# ==============================================================================

from apps.leads.models import Lead
from apps.leads.serializers import LeadCreateSerializer, LeadSerializer, LeadUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet


class LeadViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

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
