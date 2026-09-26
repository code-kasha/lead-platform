// ==============================================================================
// Route Guard
// ==============================================================================

import { Navigate, Outlet, useLocation } from "react-router-dom"

import { getAccessToken } from "../utils/token"

// Redirect to /login without a stored token, remembering where the user was
// headed. Expired tokens are handled by the API client's refresh interceptor.
export default function RequireAuth() {
	const location = useLocation()

	if (!getAccessToken()) {
		return (
			<Navigate
				to="/login"
				replace
				state={{ from: location.pathname + location.search }}
			/>
		)
	}

	return <Outlet />
}
