# ==============================================================================
# Lead Note API Views
# ==============================================================================

from typing import cast

from apps.accounts.choices import UserRole
from apps.accounts.models import User
from apps.leads.docs import lead_update_note
from apps.leads.models import LeadNote
from apps.leads.permissions import CanManageLeadNote
from apps.leads.serializers import LeadNoteSerializer, LeadNoteUpdateSerializer
from apps.leads.services import update_lead_note
from django.db.models import Q
from drf_spectacular.utils import extend_schema_view
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet


@extend_schema_view(
    partial_update=lead_update_note,
)
class LeadNoteViewSet(
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """
    Update and delete lead notes.
    """

    permission_classes = [
        IsAuthenticated,
        CanManageLeadNote,
    ]

    lookup_field = "pk"
    lookup_url_kwarg = "pk"

    serializer_classes = {
        "partial_update": LeadNoteUpdateSerializer,
        "update": LeadNoteUpdateSerializer,
        "retrieve": LeadNoteSerializer,
    }

    def get_queryset(self):
        """
        Return the notes visible to the current user.
        """

        queryset = LeadNote.objects.select_related(
            "lead",
            "author",
        )

        user = cast(
            User,
            self.request.user,
        )

        if user.role == UserRole.ADMIN:
            return queryset

        return queryset.filter(Q(author=user) | Q(lead__created_by=user) | Q(lead__assigned_to=user)).distinct()

    def get_serializer_class(self):
        """
        Return the serializer appropriate for the current action.
        """

        return self.serializer_classes.get(
            self.action,
            LeadNoteSerializer,
        )

    def perform_update(
        self,
        serializer,
    ):
        """
        Update a lead note through the business service.
        """

        update_lead_note(
            note=serializer.instance,
            content=serializer.validated_data["content"],
        )
