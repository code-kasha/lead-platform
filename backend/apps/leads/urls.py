# ==============================================================================
# Lead URL Routes
# ==============================================================================

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LeadNoteViewSet, LeadViewSet

router = DefaultRouter()

router = DefaultRouter()

router.register(
    "",
    LeadViewSet,
    basename="lead",
)

router.register(
    "notes",
    LeadNoteViewSet,
    basename="lead-note",
)

urlpatterns = [
    path("", include(router.urls)),
]
