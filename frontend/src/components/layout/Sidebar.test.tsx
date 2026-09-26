import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { createMemoryRouter, RouterProvider } from "react-router-dom"
import { describe, expect, it, vi } from "vitest"

import api from "../../api/axios"
import { getAccessToken, getRefreshToken, setTokens } from "../../utils/token"
import Sidebar from "./Sidebar"

function renderSidebar() {
	const router = createMemoryRouter(
		[
			{ path: "/dashboard", element: <Sidebar /> },
			{ path: "/login", element: <p>Login page</p> },
		],
		{ initialEntries: ["/dashboard"] },
	)

	render(
		<QueryClientProvider client={new QueryClient()}>
			<RouterProvider router={router} />
		</QueryClientProvider>,
	)
}

describe("Sidebar logout", () => {
	it("clears both tokens and returns to the login page", async () => {
		setTokens("access-1", "refresh-1")
		vi.spyOn(api, "post").mockResolvedValue({ status: 205 })

		renderSidebar()
		await userEvent.click(screen.getByRole("button", { name: "Logout" }))

		expect(await screen.findByText("Login page")).toBeInTheDocument()
		expect(getAccessToken()).toBeNull()
		expect(getRefreshToken()).toBeNull()
	})

	it("still clears tokens locally when the logout request fails", async () => {
		setTokens("access-1", "refresh-1")
		vi.spyOn(api, "post").mockRejectedValue(new Error("network down"))

		renderSidebar()
		await userEvent.click(screen.getByRole("button", { name: "Logout" }))

		expect(await screen.findByText("Login page")).toBeInTheDocument()
		expect(getAccessToken()).toBeNull()
		expect(getRefreshToken()).toBeNull()
	})
})
