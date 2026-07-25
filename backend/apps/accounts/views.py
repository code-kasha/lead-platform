# ==============================================================================
# Authentication API Views
# ==============================================================================

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .choices import UserRole
from .docs import login_schema, logout_schema, me_schema, refresh_schema, user_list_schema
from .models import User
from .serializers import LoginSerializer, LogoutSerializer, UserSerializer, UserSummarySerializer


@login_schema
class LoginView(TokenObtainPairView):
    """Authenticate users and issue JWT tokens."""

    serializer_class = LoginSerializer


@refresh_schema
class RefreshView(TokenRefreshView):
    """Issue a new access token from a valid refresh token."""

    pass


@me_schema
class MeView(generics.RetrieveAPIView):
    """Return details for the authenticated user."""

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the user associated with the current request."""

        return self.request.user


@logout_schema
class LogoutView(generics.GenericAPIView):
    """Blacklist the submitted refresh token."""

    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Invalidate the submitted refresh token."""

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            status=status.HTTP_205_RESET_CONTENT,
        )


@user_list_schema
class UserListView(generics.ListAPIView):
    """Return members available for lead assignment."""

    serializer_class = UserSummarySerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    queryset = User.objects.filter(
        role=UserRole.MEMBER,
        is_active=True,
    ).order_by(
        "first_name",
        "last_name",
    )
