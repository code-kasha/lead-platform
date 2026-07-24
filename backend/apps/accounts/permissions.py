# ==============================================================================
# Permissions for the User model
# ==============================================================================

from rest_framework.permissions import SAFE_METHODS, BasePermission

from .choices import UserRole


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class IsMember(BasePermission):
    """
    Allows access only to members.
    """

    message = "You do not have permission to perform this action."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.MEMBER


class IsAdminOrReadOnly(BasePermission):
    """
    Read for everyone.
    Write only for admins.
    """

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.role == UserRole.ADMIN
