import { screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

import { renderRoute } from "../test/render"
import { setTokens } from "../utils/token"
import PublicLeadPage from "./PublicLeadPage"

function renderPublic() {
	renderRoute(<PublicLeadPage />, { path: "/", url: "/" })
}

describe("PublicLeadPage header", () => {
	it("offers Login to visitors", () => {
		renderPublic()

		expect(screen.getByRole("link", { name: "Login" })).toHaveAttribute("href", "/login")
		expect(screen.queryByRole("link", { name: "Go to dashboard" })).not.toBeInTheDocument()
	})

	it("offers the dashboard to a signed-in user instead of Login", () => {
		setTokens("access-1", "refresh-1")
		renderPublic()

		expect(screen.getByRole("link", { name: "Go to dashboard" })).toHaveAttribute("href", "/dashboard")
		expect(screen.queryByRole("link", { name: "Login" })).not.toBeInTheDocument()
	})
})
