# ==============================================================================
# URLs for the Accounts App
# ==============================================================================

from django.urls import path

from .views import CurrentUserView, LoginView, RefreshTokenView

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(),
        name="login",
    ),
    path(
        "refresh/",
        RefreshTokenView.as_view(),
        name="refresh",
    ),
    path(
        "me/",
        CurrentUserView.as_view(),
        name="me",
    ),
]
