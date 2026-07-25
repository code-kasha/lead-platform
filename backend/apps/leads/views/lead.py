# ==============================================================================
# Lead API Views
# ==============================================================================

from typing import cast

from apps.accounts.choices import UserRole
from apps.accounts.models import User
from apps.leads.docs import (
    lead_add_note,
    lead_assign,
    lead_change_status,
    lead_create,
    lead_delete,
    lead_list,
    lead_list_activities,
    lead_list_notes,
    lead_retrieve,
    lead_update,
)
from apps.leads.filters import LeadFilter
from apps.leads.models import Lead
from apps.leads.permissions import CanAssignLead, CanChangeStatus, LeadPermission
from apps.leads.serializers import (
    AssignLeadSerializer,
    ChangeLeadStatusSerializer,
    LeadActivitySerializer,
    LeadCreateSerializer,
    LeadNoteCreateSerializer,
    LeadNoteSerializer,
    LeadSerializer,
    LeadUpdateSerializer,
)
from apps.leads.services import add_lead_note, assign_lead, change_lead_status
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


@extend_schema_view(
    list=lead_list,
    retrieve=lead_retrieve,
    create=lead_create,
    update=lead_update,
    partial_update=lead_update,
    destroy=lead_delete,
    assign=lead_assign,
    status=lead_change_status,
    add_note=lead_add_note,
    list_notes=lead_list_notes,
    list_activities=lead_list_activities,
)
class LeadViewSet(ModelViewSet):
    """Provide lead CRUD operations, filtering, search, and ordering."""

    lookup_field = "pk"
    lookup_url_kwarg = "pk"

    permission_classes = [
        LeadPermission,
    ]

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = LeadFilter

    search_fields = [
        "first_name",
        "last_name",
        "email",
        "phone",
        "company",
    ]

    ordering_fields = [
        "created_at",
        "updated_at",
        "first_name",
        "last_name",
        "status",
    ]

    ordering = [
        "-created_at",
    ]

    serializer_classes = {
        "create": LeadCreateSerializer,
        "update": LeadUpdateSerializer,
        "partial_update": LeadUpdateSerializer,
    }

    def get_queryset(self):
        """Return leads visible to the current user or an empty schema queryset."""

        queryset = Lead.objects.select_related(
            "created_by",
            "assigned_to",
        )

        user = self.request.user

        if not getattr(
            user,
            "is_authenticated",
            False,
        ):
            return queryset.none()

        user = cast(
            User,
            user,
        )

        if user.role == UserRole.ADMIN:
            return queryset

        return queryset.filter(Q(created_by=user) | Q(assigned_to=user)).distinct()

    def get_serializer_class(self):
        """Return the serializer appropriate for the current action."""

        return self.serializer_classes.get(
            self.action,
            LeadSerializer,
        )

    def create(self, request, *args, **kwargs):
        """
        Create a lead and return the full lead representation.
        """

        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        lead = serializer.save(
            created_by=request.user,
        )

        output = LeadSerializer(
            lead,
            context=self.get_serializer_context(),
        )

        return Response(
            output.data,
            status=status.HTTP_201_CREATED,
        )

    def perform_create(
        self,
        serializer,
    ):
        """Create a lead owned by the authenticated user."""

        serializer.save(
            created_by=self.request.user,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            CanAssignLead,
        ],
    )
    def assign(
        self,
        request,
        pk=None,
    ):
        """Assign the selected lead to an active member."""

        lead = self.get_object()

        serializer = AssignLeadSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        assign_lead(
            lead=lead,
            assigned_to=serializer.validated_data["assigned_to"],
            performed_by=request.user,
        )

        return Response(
            LeadSerializer(
                lead,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            CanChangeStatus,
        ],
    )
    def status(
        self,
        request,
        pk=None,
    ):
        """Change the selected lead's status."""

        lead = self.get_object()

        serializer = ChangeLeadStatusSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        change_lead_status(
            lead=lead,
            status=serializer.validated_data["status"],
            performed_by=request.user,
        )

        return Response(
            LeadSerializer(
                lead,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[
            CanChangeStatus,
        ],
        url_path="notes",
    )
    def add_note(
        self,
        request,
        pk=None,
    ):
        """Add a note to a lead."""

        lead = self.get_object()

        serializer = LeadNoteCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        note = add_lead_note(
            lead=lead,
            content=serializer.validated_data["content"],
            author=request.user,
        )

        return Response(
            LeadNoteSerializer(
                note,
                context=self.get_serializer_context(),
            ).data,
            status=status.HTTP_201_CREATED,
        )

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[
            CanChangeStatus,
        ],
        url_path="notes/list",
    )
    def list_notes(
        self,
        request,
        pk=None,
    ):
        """List all notes for a lead."""

        lead = self.get_object()

        serializer = LeadNoteSerializer(
            lead.notes.all(),
            many=True,
            context=self.get_serializer_context(),
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        detail=True,
        methods=["get"],
        permission_classes=[
            CanChangeStatus,
        ],
        url_path="activities",
    )
    def list_activities(
        self,
        request,
        pk=None,
    ):
        """
        List activities recorded for a lead.
        """
        lead = self.get_object()
        serializer = LeadActivitySerializer(
            lead.activities.all(),
            many=True,
            context=self.get_serializer_context(),
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
