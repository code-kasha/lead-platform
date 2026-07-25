# ==============================================================================
# Swagger Documentation - Leads
# ==============================================================================

from apps.common.docs import BAD_REQUEST, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from apps.leads.serializers import (
    AssignLeadSerializer,
    ChangeLeadStatusSerializer,
    LeadCreateSerializer,
    LeadNoteCreateSerializer,
    LeadNoteSerializer,
    LeadNoteUpdateSerializer,
    LeadSerializer,
    LeadUpdateSerializer,
)
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

LEAD_PK_PARAMETER = OpenApiParameter(
    name="pk",
    type=OpenApiTypes.INT,
    location=OpenApiParameter.PATH,
    description="Unique lead identifier.",
)

lead_list = extend_schema(
    tags=["Leads"],
    summary="List Leads",
    description=(
        "Returns a paginated list of leads visible to the authenticated user. "
        "Supports search, filtering and ordering."
    ),
    parameters=[
        OpenApiParameter(
            name="search",
            description="Search by first name, last name, email, phone or company.",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="status",
            description="Filter by lead status.",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="source",
            description="Filter by lead source.",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="created_by",
            description="Filter by creator.",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="assigned_to",
            description="Filter by assigned member.",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="ordering",
            description="Order by created_at, updated_at, first_name, last_name or status.",
            required=False,
            type=str,
        ),
    ],
    responses={
        200: LeadSerializer(many=True),
        401: UNAUTHORIZED,
    },
)

lead_retrieve = extend_schema(
    tags=["Leads"],
    summary="Retrieve Lead",
    description="Retrieve a single lead.",
    parameters=[LEAD_PK_PARAMETER],
    responses={
        200: LeadSerializer,
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)

lead_create = extend_schema(
    tags=["Leads"],
    summary="Create Lead",
    description=(
        "Create a new lead. " "The lead is automatically created with status NEW and is initially unassigned."
    ),
    request=LeadCreateSerializer,
    responses={
        201: LeadSerializer,
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
    },
)

lead_update = extend_schema(
    tags=["Leads"],
    summary="Update Lead",
    description=("Update lead information. " "Status changes and assignment are handled through dedicated endpoints."),
    request=LeadUpdateSerializer,
    parameters=[LEAD_PK_PARAMETER],
    responses={
        200: LeadSerializer,
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)

lead_delete = extend_schema(
    tags=["Leads"],
    summary="Delete Lead",
    description="Delete a lead.",
    parameters=[LEAD_PK_PARAMETER],
    responses={
        204: OpenApiResponse(description="Lead deleted successfully."),
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)

lead_assign = extend_schema(
    tags=["Leads"],
    summary="Assign Lead",
    description="Assign a lead to an active member.",
    request=AssignLeadSerializer,
    parameters=[LEAD_PK_PARAMETER],
    responses={
        200: LeadSerializer,
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)

lead_change_status = extend_schema(
    tags=["Leads"],
    summary="Change Lead Status",
    description="Change the status of a lead.",
    parameters=[LEAD_PK_PARAMETER],
    request=ChangeLeadStatusSerializer,
    responses={
        200: LeadSerializer,
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)

lead_add_note = extend_schema(
    tags=["Leads"],
    summary="Add Lead Note",
    description="Create a note for a lead.",
    request=LeadNoteCreateSerializer,
    responses={
        201: LeadNoteSerializer,
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)

lead_list_notes = extend_schema(
    tags=["Leads"],
    summary="List Lead Notes",
    description="Retrieve all notes for a lead.",
    responses={
        200: LeadNoteSerializer(many=True),
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)

lead_update_note = extend_schema(
    tags=["Leads"],
    operation_id="updateLeadNote",
    summary="Update Lead Note",
    description="Update the content of a lead note.",
    parameters=[
        LEAD_PK_PARAMETER,
        OpenApiParameter(
            name="note_pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Unique note identifier.",
        ),
    ],
    request=LeadNoteUpdateSerializer,
    responses={
        200: LeadNoteSerializer,
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)

lead_delete_note = extend_schema(
    tags=["Leads"],
    operation_id="deleteLeadNote",
    summary="Delete Lead Note",
    description="Delete a lead note.",
    parameters=[
        OpenApiParameter(
            name="pk",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.PATH,
            description="Unique note identifier.",
        ),
    ],
    responses={
        204: OpenApiResponse(
            description="Lead note deleted successfully.",
        ),
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)
