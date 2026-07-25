# ==============================================================================
# Lead Note API Views
# ==============================================================================

from apps.leads.models import LeadNote
from apps.leads.serializers import LeadNoteSerializer, LeadNoteUpdateSerializer
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import GenericViewSet


class LeadNoteViewSet(
    UpdateModelMixin,
    DestroyModelMixin,
    GenericViewSet,
):
    """
    Update and delete lead notes.
    """

    queryset = LeadNote.objects.select_related(
        "lead",
        "author",
    )

    lookup_field = "pk"
    lookup_url_kwarg = "pk"

    serializer_classes = {
        "partial_update": LeadNoteUpdateSerializer,
        "update": LeadNoteUpdateSerializer,
        "retrieve": LeadNoteSerializer,
    }

    def get_serializer_class(self):
        return self.serializer_classes.get(
            self.action,
            LeadNoteSerializer,
        )
