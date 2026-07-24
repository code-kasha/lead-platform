# ==============================================================================
# drf-spectacular Configuration
# ==============================================================================

SPECTACULAR_SETTINGS = {
    "TITLE": "Lead Management API",
    "DESCRIPTION": ("REST API for managing leads, assignments, notes, activities " "and authentication."),
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "SORT_OPERATIONS": False,
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
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
