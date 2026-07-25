# ==============================================================================
# Lead Note API Views
# ==============================================================================

from rest_framework.viewsets import GenericViewSet


class LeadNoteViewSet(GenericViewSet):
    """
    API endpoints for updating and deleting lead notes.
    """

    lookup_field = "pk"
    lookup_url_kwarg = "pk"
