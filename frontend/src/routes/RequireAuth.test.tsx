import { render, screen } from "@testing-library/react"
import { createMemoryRouter, RouterProvider, useLocation } from "react-router-dom"
import { describe, expect, it } from "vitest"

import { setTokens } from "../utils/token"
import RequireAuth from "./RequireAuth"

function LoginProbe() {
	const location = useLocation()

	return <p>Login page, from {(location.state as { from?: string } | null)?.from}</p>
}

function renderAt(path: string) {
	const router = createMemoryRouter(
		[
			{ path: "/login", element: <LoginProbe /> },
			{
				element: <RequireAuth />,
				children: [{ path: "/leads/:id", element: <p>Lead detail</p> }],
			},
		],
		{ initialEntries: [path] },
	)

	render(<RouterProvider router={router} />)
}

describe("RequireAuth", () => {
	it("redirects to /login and remembers the requested page when logged out", () => {
		renderAt("/leads/7?tab=notes")

		expect(screen.getByText("Login page, from /leads/7?tab=notes")).toBeInTheDocument()
		expect(screen.queryByText("Lead detail")).not.toBeInTheDocument()
	})

	it("renders the protected page when a token is stored", () => {
		setTokens("access-1", "refresh-1")

		renderAt("/leads/7")

		expect(screen.getByText("Lead detail")).toBeInTheDocument()
	})
})
