import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { createMemoryRouter, RouterProvider } from "react-router-dom"
import { describe, expect, it, vi } from "vitest"

import api from "../../api/axios"
import { getAccessToken, getRefreshToken } from "../../utils/token"
import LoginPage from "./LoginPage"

function renderLogin() {
	const router = createMemoryRouter(
		[
			{ path: "/login", element: <LoginPage /> },
			{ path: "/dashboard", element: <p>Dashboard</p> },
		],
		{ initialEntries: ["/login"] },
	)

	render(<RouterProvider router={router} />)
}

describe("LoginPage", () => {
	it("posts the credentials, stores the tokens and opens the dashboard", async () => {
		const post = vi.spyOn(api, "post").mockResolvedValue({
			data: { access: "access-1", refresh: "refresh-1" },
		})

		renderLogin()
		await userEvent.type(screen.getByPlaceholderText("Email"), "user@test.com")
		await userEvent.type(screen.getByPlaceholderText("Password"), "password123")
		await userEvent.click(screen.getByRole("button", { name: "Login" }))

		expect(await screen.findByText("Dashboard")).toBeInTheDocument()
		expect(post).toHaveBeenCalledWith("/auth/login/", {
			email: "user@test.com",
			password: "password123",
		})
		expect(getAccessToken()).toBe("access-1")
		expect(getRefreshToken()).toBe("refresh-1")
	})
})
