# ==============================================================================
# Swagger Documentation - Authentication
# ==============================================================================

from apps.accounts.serializers import UserSerializer
from apps.common.docs import BAD_REQUEST, UNAUTHORIZED
from apps.common.examples import LOGIN_SUCCESS, TOKEN_REFRESH
from apps.common.examples import UNAUTHORIZED as UNAUTHORIZED_EXAMPLE
from apps.common.serializers import AccessTokenSerializer, LoginRequestSerializer, TokenSerializer
from drf_spectacular.utils import extend_schema

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
    description="Generate a new access token using a valid refresh token.",
    responses={
        200: AccessTokenSerializer,
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
    description=("Invalidate the supplied refresh token by adding it to the " "JWT blacklist."),
    responses={
        205: None,
        400: BAD_REQUEST,
        401: UNAUTHORIZED,
    },
)
