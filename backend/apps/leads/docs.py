# ==============================================================================
# Swagger Documentation
# ==============================================================================

from apps.leads.serializers import LeadCreateSerializer, LeadSerializer, LeadUpdateSerializer
from drf_spectacular.utils import OpenApiParameter, OpenApiResponse, extend_schema

lead_list = extend_schema(
    tags=["Leads"],
    summary="List Leads",
    description=("Returns a paginated list of leads."),
    parameters=[
        OpenApiParameter(
            name="search",
            description="Search by name, email or company.",
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
            name="ordering",
            description="Sort results (created_at, first_name, company). Prefix with '-' for descending.",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="page",
            description="Page number.",
            required=False,
            type=int,
        ),
        OpenApiParameter(
            name="page_size",
            description="Number of results per page.",
            required=False,
            type=int,
        ),
    ],
    responses={
        200: LeadSerializer(many=True),
    },
)

lead_retrieve = extend_schema(
    tags=["Leads"],
    summary="Retrieve Lead",
    description="Retrieve a single lead.",
    responses={
        200: LeadSerializer,
        404: OpenApiResponse(description="Lead not found"),
    },
)

lead_create = extend_schema(
    tags=["Leads"],
    summary="Create Lead",
    description="Create a new lead.",
    request=LeadCreateSerializer,
    responses={
        201: LeadSerializer,
        400: OpenApiResponse(description="Validation error"),
    },
)

lead_update = extend_schema(
    tags=["Leads"],
    summary="Update Lead",
    description="Update an existing lead.",
    request=LeadUpdateSerializer,
    responses={
        200: LeadSerializer,
        400: OpenApiResponse(description="Validation error"),
        404: OpenApiResponse(description="Lead not found"),
    },
)

lead_delete = extend_schema(
    tags=["Leads"],
    summary="Delete Lead",
    description="Delete a lead.",
    responses={
        204: OpenApiResponse(description="Lead deleted"),
        404: OpenApiResponse(description="Lead not found"),
    },
)
