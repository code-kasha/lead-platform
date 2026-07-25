# ==============================================================================
# Authentication URL Routes
# ==============================================================================

from django.urls import path

from .views import LoginView, LogoutView, MeView, RefreshView, UserListView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        LogoutView.as_view(),
        name="logout",
    ),
    path(
        "refresh/",
        RefreshView.as_view(),
        name="refresh",
    ),
    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),
    path(
        "users/",
        UserListView.as_view(),
        name="user-list",
    ),
]
