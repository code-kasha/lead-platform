# ==============================================================================
# Lead Note API Views
# ==============================================================================

from typing import cast

from apps.accounts.choices import UserRole
from apps.accounts.models import User
from apps.leads.docs import lead_delete_note, lead_replace_note, lead_update_note
from apps.leads.services import delete_lead_note, update_lead_note
from apps.leads.models import LeadNote
from apps.leads.permissions import CanManageLeadNote
from apps.leads.serializers import LeadNoteSerializer, LeadNoteUpdateSerializer
from django.db.models import Q
from django.db.models.query import QuerySet
from drf_spectacular.utils import extend_schema_view
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


@extend_schema_view(
    update=lead_replace_note,
    partial_update=lead_update_note,
    destroy=lead_delete_note,
)
class LeadNoteViewSet(
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """Provide update and delete operations for lead notes."""

    queryset = LeadNote.objects.select_related(
        "lead",
        "author",
    )

    permission_classes = [
        IsAuthenticated,
        CanManageLeadNote,
    ]

    lookup_field = "pk"
    lookup_url_kwarg = "pk"

    serializer_class = LeadNoteSerializer

    serializer_classes = {
        "partial_update": LeadNoteUpdateSerializer,
        "update": LeadNoteUpdateSerializer,
        "retrieve": LeadNoteSerializer,
    }

    def get_queryset(self) -> QuerySet[LeadNote]:
        """Return notes visible to the current user."""

        request = getattr(
            self,
            "request",
            None,
        )

        if request is None or not hasattr(request, "user"):
            return self.queryset

        user = cast(
            User,
            request.user,
        )

        if not user.is_authenticated:
            return self.queryset.none()

        if user.role == UserRole.ADMIN:
            return self.queryset

        return self.queryset.filter(Q(author=user) | Q(lead__created_by=user) | Q(lead__assigned_to=user)).distinct()

    def perform_update(self, serializer) -> None:
        """Save the edit through the notes service."""

        serializer.instance = update_lead_note(
            note=serializer.instance,
            # A PATCH may omit content; keep the current text then
            content=serializer.validated_data.get("content", serializer.instance.content),
        )

    def perform_destroy(self, instance: LeadNote) -> None:
        """Delete through the notes service."""

        delete_lead_note(note=instance)
