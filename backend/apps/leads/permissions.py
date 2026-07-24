# ==============================================================================
# Lead Permissions
# ==============================================================================

from apps.accounts.choices import UserRole
from rest_framework.permissions import SAFE_METHODS, BasePermission


class LeadPermission(BasePermission):
    """
    Object-level permissions for Lead CRUD operations.
    """

    message = "You do not have permission to access this lead."

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        # Administrators have unrestricted access.
        if request.user.role == UserRole.ADMIN:
            return True

        # Only members are supported beyond this point.
        if request.user.role != UserRole.MEMBER:
            return False

        # Members may view leads they created or that are assigned to them.
        if request.method in SAFE_METHODS:
            return obj.created_by == request.user or obj.assigned_to == request.user

        # Members may update leads they created or that are assigned to them.
        if request.method in ("PUT", "PATCH"):
            return obj.created_by == request.user or obj.assigned_to == request.user

        # Members cannot delete leads.
        return False


class CanAssignLead(BasePermission):
    """
    Only administrators can assign leads.
    """

    message = "Only administrators can assign leads."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == UserRole.ADMIN


class CanChangeStatus(BasePermission):
    """
    Placeholder for lead status workflow permissions.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated
