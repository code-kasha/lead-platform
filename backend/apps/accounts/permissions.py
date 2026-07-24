# ==============================================================================
# Role-based Permissions
# ==============================================================================

from rest_framework.permissions import BasePermission

from .choices import UserRole


class IsAdmin(BasePermission):
    """
    Allows access only to administrators.
    """

    message = "Administrator privileges are required."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.ADMIN


class IsMember(BasePermission):
    """
    Allows access only to members.
    """

    message = "Member privileges are required."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.MEMBER


class IsAdminOrMember(BasePermission):
    """
    Allows access to any authenticated user.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in (
            UserRole.ADMIN,
            UserRole.MEMBER,
        )
