# ==============================================================================
# Role-based Permissions
# ==============================================================================

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from .choices import UserRole


class IsAdmin(BasePermission):
    """Allow access only to administrators."""

    message = "Administrator privileges are required."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return whether the request user is an administrator."""

        return request.user.is_authenticated and request.user.role == UserRole.ADMIN


class IsMember(BasePermission):
    """Allow access only to members."""

    message = "Member privileges are required."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return whether the request user is a member."""

        return request.user.is_authenticated and request.user.role == UserRole.MEMBER


class IsAdminOrMember(BasePermission):
    """Allow access to authenticated administrators and members."""

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return whether the request user has a supported role."""

        return request.user.is_authenticated and request.user.role in (
            UserRole.ADMIN,
            UserRole.MEMBER,
        )
