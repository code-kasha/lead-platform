# ==============================================================================
# Lead Permissions
# ==============================================================================

from apps.accounts.choices import UserRole
from rest_framework.permissions import SAFE_METHODS, BasePermission


class LeadPermission(BasePermission):
    """
    Object-level permissions for the Lead API.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Everyone can view leads
        if request.method in SAFE_METHODS:
            return True

        # Admins have full access
        if request.user.role == UserRole.ADMIN:
            return True

        # Members can update leads they created or are assigned to
        if request.user.role == UserRole.MEMBER:
            if request.method in ("PUT", "PATCH"):
                return obj.created_by == request.user or obj.assigned_to == request.user

            # Members cannot delete
            return False

        return False
