# ==============================================================================
# Authentication API Views
# ==============================================================================

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .docs import login_schema, logout_schema, me_schema, refresh_schema
from .serializers import LoginSerializer, LogoutSerializer, UserSerializer


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


@logout_schema
class LogoutView(generics.GenericAPIView):
    """
    Blacklist a refresh token.
    """

    serializer_class = LogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_205_RESET_CONTENT)
