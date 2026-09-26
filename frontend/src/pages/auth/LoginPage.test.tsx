import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { AxiosError, type AxiosResponse } from "axios"
import { createMemoryRouter, RouterProvider } from "react-router-dom"
import toast from "react-hot-toast"
import { describe, expect, it, vi } from "vitest"

import api from "../../api/axios"
import { getAccessToken, getRefreshToken, setTokens } from "../../utils/token"
import LoginPage from "./LoginPage"

vi.mock("react-hot-toast", () => ({ default: { success: vi.fn(), error: vi.fn() } }))

function renderLogin(from?: string) {
	const router = createMemoryRouter(
		[
			{ path: "/login", element: <LoginPage /> },
			{ path: "/dashboard", element: <p>Dashboard</p> },
			{ path: "/leads/:id", element: <p>Lead detail</p> },
		],
		{ initialEntries: [{ pathname: "/login", state: from ? { from } : null }] },
	)

	render(<RouterProvider router={router} />)
}

async function submit(email = "user@test.com", password = "password123") {
	await userEvent.type(screen.getByPlaceholderText("Email"), email)
	await userEvent.type(screen.getByPlaceholderText("Password"), password)
	await userEvent.click(screen.getByRole("button", { name: "Login" }))
}

function httpError(status: number, data: unknown) {
	const response = { status, data } as AxiosResponse

	return new AxiosError("Request failed", undefined, undefined, undefined, response)
}

describe("LoginPage", () => {
	it("posts the credentials, stores the tokens and opens the dashboard", async () => {
		const post = vi.spyOn(api, "post").mockResolvedValue({
			data: { access: "access-1", refresh: "refresh-1" },
		})

		renderLogin()
		await submit()

		expect(await screen.findByText("Dashboard")).toBeInTheDocument()
		expect(post).toHaveBeenCalledWith("/auth/login/", {
			email: "user@test.com",
			password: "password123",
		})
		expect(getAccessToken()).toBe("access-1")
		expect(getRefreshToken()).toBe("refresh-1")
	})

	it("returns to the page the route guard redirected from", async () => {
		vi.spyOn(api, "post").mockResolvedValue({
			data: { access: "access-1", refresh: "refresh-1" },
		})

		renderLogin("/leads/7")
		await submit()

		expect(await screen.findByText("Lead detail")).toBeInTheDocument()
	})

	it("shows the server's message for rejected credentials", async () => {
		vi.spyOn(api, "post").mockRejectedValue(
			httpError(401, { detail: "No active account found with the given credentials" }),
		)

		renderLogin()
		await submit("user@test.com", "wrong")

		expect(await screen.findByRole("alert")).toHaveTextContent(
			"No active account found with the given credentials",
		)
		expect(getAccessToken()).toBeNull()
		expect(screen.getByRole("button", { name: "Login" })).toBeEnabled()
	})

	it("asks for valid input when the server rejects the form", async () => {
		vi.spyOn(api, "post").mockRejectedValue(
			httpError(400, { email: ["Enter a valid email address."] }),
		)

		renderLogin()
		await submit("not-an-email")

		expect(await screen.findByRole("alert")).toHaveTextContent(
			"Enter a valid email address and password.",
		)
	})

	it("shows a generic message when the server is unreachable", async () => {
		vi.spyOn(api, "post").mockRejectedValue(new AxiosError("Network Error"))

		renderLogin()
		await submit()

		expect(await screen.findByRole("alert")).toHaveTextContent(
			"Unable to sign in right now. Please try again.",
		)
	})

	it("clears the previous error when retrying", async () => {
		vi.spyOn(api, "post")
			.mockRejectedValueOnce(httpError(401, { detail: "Bad credentials" }))
			.mockResolvedValueOnce({ data: { access: "access-1", refresh: "refresh-1" } })

		renderLogin()
		await submit("user@test.com", "wrong")
		expect(await screen.findByRole("alert")).toBeInTheDocument()

		await userEvent.clear(screen.getByPlaceholderText("Password"))
		await userEvent.type(screen.getByPlaceholderText("Password"), "password123")
		await userEvent.click(screen.getByRole("button", { name: "Login" }))

		expect(await screen.findByText("Dashboard")).toBeInTheDocument()
		expect(screen.queryByRole("alert")).not.toBeInTheDocument()
	})
})

describe("LoginPage feedback and redirects", () => {
	it("confirms a successful sign-in and shows progress while signing in", async () => {
		let resolve!: (value: unknown) => void
		vi.spyOn(api, "post").mockReturnValue(new Promise((r) => (resolve = r)) as never)

		renderLogin()
		await submit()

		expect(screen.getByRole("button", { name: "Signing in..." })).toBeDisabled()

		resolve({ data: { access: "access-1", refresh: "refresh-1" } })

		expect(await screen.findByText("Dashboard")).toBeInTheDocument()
		expect(toast.success).toHaveBeenCalledWith("Signed in successfully.")
	})

	it("sends an already signed-in user to the dashboard", async () => {
		setTokens("access-1", "refresh-1")
		const post = vi.spyOn(api, "post")

		renderLogin()

		expect(await screen.findByText("Dashboard")).toBeInTheDocument()
		expect(screen.queryByPlaceholderText("Password")).not.toBeInTheDocument()
		expect(post).not.toHaveBeenCalled()
	})

	it("sends an already signed-in user back to the page they were headed for", async () => {
		setTokens("access-1", "refresh-1")

		renderLogin("/leads/7")

		expect(await screen.findByText("Lead detail")).toBeInTheDocument()
	})
})
