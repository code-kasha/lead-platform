import { screen, within } from "@testing-library/react"
import type { AxiosResponse } from "axios"
import { describe, expect, it, vi } from "vitest"

import api from "../../api/axios"
import { makeLead } from "../../test/fixtures"
import { renderRoute } from "../../test/render"
import LeadListPage from "./LeadListPage"

function renderList() {
	renderRoute(<LeadListPage />, { path: "/leads", url: "/leads" })
}

function respondWith(results: ReturnType<typeof makeLead>[]) {
	vi.spyOn(api, "get").mockResolvedValue({
		data: { count: results.length, next: null, previous: null, results },
	} as AxiosResponse)
}

describe("LeadListPage", () => {
	it("lists each lead with its company, email, status and a link to it", async () => {
		respondWith([
			makeLead({ id: 7, status: "QUALIFIED" }),
			makeLead({ id: 8, first_name: "Grace", last_name: "Hopper", email: "grace@example.com", company: "" }),
		])
		renderList()

		const ada = (await screen.findByText("Ada Lovelace")).closest("tr")!
		expect(within(ada).getByText("Engines Ltd")).toBeInTheDocument()
		expect(within(ada).getByText("ada@example.com")).toBeInTheDocument()
		expect(within(ada).getByText("Qualified")).toBeInTheDocument()
		expect(within(ada).getByRole("link", { name: "View" })).toHaveAttribute("href", "/leads/7")

		const grace = screen.getByText("Grace Hopper").closest("tr")!
		expect(within(grace).getByText("-")).toBeInTheDocument()
		expect(within(grace).getByRole("link", { name: "View" })).toHaveAttribute("href", "/leads/8")
	})

	it("shows an empty message when there are no leads", async () => {
		respondWith([])
		renderList()

		expect(await screen.findByText("No leads found.")).toBeInTheDocument()
	})

	it("shows an error when the leads cannot be loaded", async () => {
		vi.spyOn(api, "get").mockRejectedValue(new Error("500"))
		renderList()

		expect(await screen.findByText("Failed to load leads.")).toBeInTheDocument()
	})

	it("links to the new lead form", async () => {
		respondWith([])
		renderList()

		expect(await screen.findByRole("link", { name: "New Lead" })).toHaveAttribute("href", "/leads/new")
	})
})
