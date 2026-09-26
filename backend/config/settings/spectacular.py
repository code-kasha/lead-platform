# ==============================================================================
# drf-spectacular Configuration
# ==============================================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "Lead Management API",
    "DESCRIPTION": ("REST API for managing leads, assignments, notes, activities " "and authentication."),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": True,
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
    # Serve Swagger UI and ReDoc from the pinned sidecar package, not a CDN
    "SWAGGER_UI_DIST": "SIDECAR",
    "SWAGGER_UI_FAVICON_HREF": "SIDECAR",
    "REDOC_DIST": "SIDECAR",
    "TAGS": [
        {
            "name": "Authentication",
            "description": ("Endpoints for user authentication and JWT token management."),
        },
        {
            "name": "Leads",
            "description": ("Create, update, assign and manage sales leads."),
        },
    ],
}
