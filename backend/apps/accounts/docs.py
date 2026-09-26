# ==============================================================================
# Swagger Documentation - Authentication
# ==============================================================================

from apps.common.docs import BAD_REQUEST, UNAUTHORIZED
from apps.common.examples import LOGIN_SUCCESS, TOKEN_REFRESH
from apps.common.examples import UNAUTHORIZED as UNAUTHORIZED_EXAMPLE
from apps.common.serializers import LoginRequestSerializer, TokenSerializer
from drf_spectacular.utils import extend_schema

from .serializers import LogoutSerializer, UserSerializer, UserSummarySerializer

login_schema = extend_schema(
    tags=["Authentication"],
    summary="Login",
    description=(
        "Authenticate a user using their email address and password. " "Returns JWT access and refresh tokens."
    ),
    request=LoginRequestSerializer,
    responses={
        200: TokenSerializer,
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
    },
    examples=[
        LOGIN_SUCCESS,
        UNAUTHORIZED_EXAMPLE,
    ],
)


refresh_schema = extend_schema(
    tags=["Authentication"],
    summary="Refresh Access Token",
    description=(
        "Generate a new access token using a valid refresh token. Refresh tokens are rotated: "
        "the response includes a new refresh token and the submitted one is blacklisted."
    ),
    responses={
        200: TokenSerializer,
        401: UNAUTHORIZED,
    },
    examples=[
        TOKEN_REFRESH,
        UNAUTHORIZED_EXAMPLE,
    ],
)


me_schema = extend_schema(
    tags=["Authentication"],
    summary="Current User",
    description="Retrieve details of the currently authenticated user.",
    responses={
        200: UserSerializer,
        401: UNAUTHORIZED,
    },
)


logout_schema = extend_schema(
    tags=["Authentication"],
    summary="Logout",
    description=("Blacklist the supplied refresh token so it cannot be used " "to obtain new access tokens."),
    request=LogoutSerializer,
    responses={
        205: None,
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
    },
)


user_list_schema = extend_schema(
    tags=["Users"],
    summary="List Users",
    description="Return all active members available for lead assignment.",
    responses={
        200: UserSummarySerializer(many=True),
        401: UNAUTHORIZED,
    },
)
