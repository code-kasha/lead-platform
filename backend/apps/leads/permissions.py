# ==============================================================================
# Lead Permissions
# ==============================================================================

from apps.accounts.choices import UserRole
from apps.leads.models import Lead, LeadNote
from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView


class LeadPermission(BasePermission):
    """Control access to lead CRUD operations."""

    message = "You do not have permission to access this lead."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return whether the request is authenticated."""

        return request.user.is_authenticated

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Lead,
    ) -> bool:
        """Return whether the user may access the specified lead."""

        if request.user.role == UserRole.ADMIN:
            return True

        if request.user.role != UserRole.MEMBER:
            return False

        if request.method in SAFE_METHODS:
            return obj.created_by == request.user or obj.assigned_to == request.user

        if request.method in ("PUT", "PATCH"):
            return obj.created_by == request.user or obj.assigned_to == request.user

        return False


class CanAssignLead(BasePermission):
    """Allow only administrators to assign leads."""

    message = "Only administrators can assign leads."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return whether the request user is an administrator."""

        return request.user.is_authenticated and request.user.role == UserRole.ADMIN

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Lead,
    ) -> bool:
        """Apply the administrator requirement to object access."""

        return self.has_permission(request, view)


class CanChangeStatus(BasePermission):
    """Control which users may change a lead's status."""

    message = "You do not have permission to change this lead's status."

    def has_permission(self, request: Request, view: APIView) -> bool:
        """Return whether the request is authenticated."""

        return request.user.is_authenticated

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: Lead,
    ) -> bool:
        """Return whether the user may change the lead's status."""

        if request.user.role == UserRole.ADMIN:
            return True

        return obj.created_by == request.user or obj.assigned_to == request.user


class CanManageLeadNote(BasePermission):
    """
    Allow administrators or the note author to edit or delete a note.
    """

    message = "You do not have permission to modify this note."

    def has_object_permission(
        self,
        request: Request,
        view: APIView,
        obj: LeadNote,
    ) -> bool:
        if request.user.role == UserRole.ADMIN:
            return True

        return obj.author == request.user
