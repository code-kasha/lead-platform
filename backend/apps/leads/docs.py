# ==============================================================================
# Swagger Documentation - Leads
# ==============================================================================

from apps.common.docs import BAD_REQUEST, FORBIDDEN, NOT_FOUND, UNAUTHORIZED
from apps.leads.serializers import (
    AssignLeadSerializer,
    ChangeLeadStatusSerializer,
    LeadActivitySerializer,
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
    summary="List visible leads",
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
    summary="Retrieve a lead",
    description="Retrieve a single lead that is visible to the authenticated user.",
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
    summary="Create a lead",
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
    summary="Update a lead",
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
    summary="Delete a lead",
    description="Permanently delete a lead visible to the authenticated user.",
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
    summary="Assign a lead",
    description="Assign a lead to an active member. Administrator access is required.",
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
    summary="Change a lead's status",
    description="Change a lead's status when the requested transition is allowed.",
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
    summary="Add a lead note",
    description="Create a note for a lead and record the related activity.",
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
    summary="List lead notes",
    description="Retrieve all notes for a lead visible to the authenticated user.",
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
    summary="Update a lead note",
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
    summary="Delete a lead note",
    description="Permanently delete a lead note the authenticated user may manage.",
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

lead_list_activities = extend_schema(
    tags=["Leads"],
    summary="List lead activities",
    description="Retrieve activities recorded for a lead visible to the authenticated user.",
    parameters=[
        LEAD_PK_PARAMETER,
    ],
    responses={
        200: LeadActivitySerializer(many=True),
        401: UNAUTHORIZED,
        403: FORBIDDEN,
        404: NOT_FOUND,
    },
)
