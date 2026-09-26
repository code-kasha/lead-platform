import { screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

import { renderRoute } from "../../test/render"
import DashboardPage from "./DashboardPage"

describe("DashboardPage", () => {
	it("links to the API docs of the configured backend, not localhost", () => {
		renderRoute(<DashboardPage />, { path: "/dashboard", url: "/dashboard" })

		// Vitest pins VITE_API_URL to http://api.test/api
		expect(screen.getByRole("link", { name: "Open Swagger" })).toHaveAttribute(
			"href",
			"http://api.test/api/docs/",
		)
	})
})
