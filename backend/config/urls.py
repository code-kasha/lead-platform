# ==============================================================================
# URL config for the project.
# ==============================================================================

from django.contrib import admin
from django.urls import include, path, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from apps.common.views import frontend_index

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/auth/",
        include("apps.accounts.urls"),
    ),
    path(
        "api/leads/",
        include("apps.leads.urls"),
    ),
    # --------------------------------------------------------------------------
    # API Documentation
    # --------------------------------------------------------------------------
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
    # --------------------------------------------------------------------------
    # Frontend: every other path is a client-side route (must stay last)
    # --------------------------------------------------------------------------
    re_path(
        r"^(?!api/|admin/|static/).*$",
        frontend_index,
        name="frontend",
    ),
]
