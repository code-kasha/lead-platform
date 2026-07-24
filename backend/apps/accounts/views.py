# ==============================================================================
# Authentication API Views
# ==============================================================================

from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .docs import login_schema, me_schema, refresh_schema
from .serializers import LoginSerializer, UserSerializer


@login_schema
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


@refresh_schema
class RefreshView(TokenRefreshView):
    pass


@me_schema
class MeView(generics.RetrieveAPIView):
    """
    Return the currently authenticated user.
    """

    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
