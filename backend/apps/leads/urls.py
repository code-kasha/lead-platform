# ==============================================================================
# Lead URL Routes
# ==============================================================================

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LeadNoteViewSet, LeadViewSet, PublicLeadCreateView

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
    path(
        "public/",
        PublicLeadCreateView.as_view(),
        name="public-lead-create",
    ),
    path("", include(router.urls)),
]
