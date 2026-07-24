# ==============================================================================
# Shared OpenAPI Responses
# ==============================================================================

from apps.common.serializers import ErrorSerializer
from drf_spectacular.utils import OpenApiResponse

BAD_REQUEST = OpenApiResponse(
    response=ErrorSerializer,
    description="The request could not be processed.",
)

UNAUTHORIZED = OpenApiResponse(
    response=ErrorSerializer,
    description="Authentication credentials are invalid or missing.",
)

FORBIDDEN = OpenApiResponse(
    response=ErrorSerializer,
    description="You do not have permission to perform this action.",
)

NOT_FOUND = OpenApiResponse(
    response=ErrorSerializer,
    description="Requested resource was not found.",
)
