// ==============================================================================
// Session Helpers
// ==============================================================================

import { clearTokens } from "./token"

// Drop the local session and send the user to the login page. A full page
// load resets in-memory state (query cache, forms) belonging to the old user.
export function endSession() {
	clearTokens()

	if (window.location.pathname !== "/login") {
		window.location.assign("/login")
	}
}
