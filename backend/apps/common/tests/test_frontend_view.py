# ==============================================================================
# Frontend (SPA) Route Tests
# ==============================================================================

import tempfile
from pathlib import Path

from django.test import TestCase, override_settings


class FrontendRouteTests(TestCase):
    """Verify client-side routes get index.html without shadowing the API."""

    def setUp(self) -> None:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.dist = Path(tmp.name)
        (self.dist / "index.html").write_text("<!doctype html><div id=root></div>")

    def test_client_routes_get_index_html(self) -> None:
        """Ensure deep links like /leads/7 survive a reload."""

        with override_settings(FRONTEND_DIST=self.dist):
            for path in ["/", "/login", "/leads/7", "/leads?page=2"]:
                response = self.client.get(path)

                self.assertEqual(response.status_code, 200, path)
                self.assertIn(b"<div id=root>", b"".join(response.streaming_content))
                self.assertEqual(response["Cache-Control"], "no-cache")

    def test_api_paths_are_not_swallowed(self) -> None:
        """Ensure unknown API and admin URLs 404 instead of returning the app."""

        with override_settings(FRONTEND_DIST=self.dist):
            for path in ["/api/does-not-exist/", "/static/missing.css"]:
                response = self.client.get(path)

                self.assertEqual(response.status_code, 404, path)
                self.assertFalse(response.streaming, path)

    def test_missing_build_is_a_404(self) -> None:
        """Ensure development (no build) doesn't crash on non-API paths."""

        with override_settings(FRONTEND_DIST=self.dist / "missing"):
            response = self.client.get("/leads/7")

        self.assertEqual(response.status_code, 404)
