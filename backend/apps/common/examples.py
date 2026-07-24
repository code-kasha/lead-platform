# ==============================================================================
# Shared OpenAPI Examples
# ==============================================================================

from drf_spectacular.utils import OpenApiExample

LOGIN_SUCCESS = OpenApiExample(
    "Login Success",
    response_only=True,
    value={
        "access": "<jwt-access-token>",
        "refresh": "<jwt-refresh-token>",
    },
)

TOKEN_REFRESH = OpenApiExample(
    "Token Refresh",
    response_only=True,
    value={
        "access": "<new-access-token>",
    },
)

UNAUTHORIZED = OpenApiExample(
    "Unauthorized",
    response_only=True,
    status_codes=["401"],
    value={"detail": "No active account found with the given credentials"},
)

PERMISSION_DENIED = OpenApiExample(
    "Permission Denied",
    response_only=True,
    status_codes=["403"],
    value={"detail": "You do not have permission to perform this action."},
)

NOT_FOUND = OpenApiExample(
    "Not Found",
    response_only=True,
    status_codes=["404"],
    value={"detail": "Not found."},
)

VALIDATION_ERROR = OpenApiExample(
    "Validation Error",
    response_only=True,
    status_codes=["400"],
    value={"email": ["This field is required."]},
)
