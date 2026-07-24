# ==============================================================================
# Views for the User model
# ==============================================================================

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import LoginSerializer, UserSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class RefreshTokenView(TokenRefreshView):
    pass


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user
