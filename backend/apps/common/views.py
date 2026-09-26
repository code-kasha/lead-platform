# ==============================================================================
# Views for the Common app
# ==============================================================================

from django.conf import settings
from django.http import FileResponse, Http404, HttpRequest

# ==============================================================================
# Frontend (single-page app)
# ==============================================================================


def frontend_index(request: HttpRequest) -> FileResponse:
    """Serve the built frontend's index.html so client-side routes survive a reload.

    In the Docker image the built frontend lives in FRONTEND_DIST; WhiteNoise
    serves its asset files, and every other non-API path gets index.html so
    React Router can render it. In development the directory doesn't exist
    and the Vite dev server serves the frontend instead.
    """

    index = settings.FRONTEND_DIST / "index.html"

    if not index.is_file():
        raise Http404("Frontend build not found.")

    response = FileResponse(index.open("rb"), content_type="text/html")

    # Always revalidate: index.html points at the current hashed asset files
    response["Cache-Control"] = "no-cache"

    return response
