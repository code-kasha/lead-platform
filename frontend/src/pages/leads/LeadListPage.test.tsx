import { screen, waitFor, within } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { AxiosError } from "axios"
import type { AxiosResponse } from "axios"
import { describe, expect, it, vi } from "vitest"

import api from "../../api/axios"
import { makeLead } from "../../test/fixtures"
import { renderRoute } from "../../test/render"
import LeadListPage from "./LeadListPage"

function renderList(url = "/leads") {
	return renderRoute(<LeadListPage />, { path: "/leads", url })
}

// Fake paginated endpoint over `total` leads, 20 per page, mirroring DRF
function paginatedLeads(total: number) {
	return vi.spyOn(api, "get").mockImplementation((_url: string, config?: { params?: Record<string, number> }) => {
		const page = config?.params?.page ?? 1
		const size = config?.params?.page_size ?? 20
		const pages = Math.max(1, Math.ceil(total / size))

		if (page > pages) {
			return Promise.reject(
				new AxiosError("Not Found", undefined, undefined, undefined, {
					status: 404,
					data: { detail: "Invalid page." },
				} as AxiosResponse),
			)
		}

		const start = (page - 1) * size
		const results = Array.from({ length: Math.min(size, total - start) }, (_, i) =>
			makeLead({ id: start + i + 1, first_name: "Lead", last_name: String(start + i + 1) }),
		)

		return Promise.resolve({
			data: {
				count: total,
				next: page < pages ? `?page=${page + 1}` : null,
				previous: page > 1 ? `?page=${page - 1}` : null,
				results,
			},
		} as AxiosResponse)
	})
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

describe("LeadListPage pagination", () => {
	it("requests the first page of 20 by default", async () => {
		const get = paginatedLeads(45)
		renderList()

		await screen.findByText("Lead 1")
		expect(get).toHaveBeenCalledWith("/leads/", { params: { page: 1, page_size: 20 } })
		expect(screen.getByText("Showing 1–20 of 45")).toBeInTheDocument()
		expect(screen.getByRole("button", { name: "Previous" })).toBeDisabled()
		expect(screen.getByRole("button", { name: "Next" })).toBeEnabled()
	})

	it("moves to the next page and records it in the URL", async () => {
		paginatedLeads(45)
		const { router } = renderList()
		await screen.findByText("Lead 1")

		await userEvent.click(screen.getByRole("button", { name: "Next" }))

		expect(await screen.findByText("Lead 21")).toBeInTheDocument()
		expect(screen.queryByText("Lead 1")).not.toBeInTheDocument()
		expect(screen.getByText("Showing 21–40 of 45")).toBeInTheDocument()
		expect(router.state.location.search).toBe("?page=2")
	})

	it("opens the page given in the URL and stops at the last page", async () => {
		paginatedLeads(45)
		renderList("/leads?page=3")

		expect(await screen.findByText("Lead 41")).toBeInTheDocument()
		expect(screen.getByText("Showing 41–45 of 45")).toBeInTheDocument()
		expect(screen.getByRole("button", { name: "Next" })).toBeDisabled()

		await userEvent.click(screen.getByRole("button", { name: "Previous" }))
		expect(await screen.findByText("Lead 21")).toBeInTheDocument()
	})

	it("hides the pager when everything fits on one page", async () => {
		paginatedLeads(3)
		renderList()

		await screen.findByText("Lead 1")
		expect(screen.queryByRole("button", { name: "Next" })).not.toBeInTheDocument()
	})

	it("treats a malformed page number as the first page", async () => {
		const get = paginatedLeads(45)
		renderList("/leads?page=abc")

		await screen.findByText("Lead 1")
		expect(get).toHaveBeenCalledWith("/leads/", { params: { page: 1, page_size: 20 } })
	})

	it("offers a way back when the page no longer exists", async () => {
		paginatedLeads(45)
		const { router } = renderList("/leads?page=9")

		expect(await screen.findByText("That page doesn't exist.")).toBeInTheDocument()
		await userEvent.click(screen.getByRole("link", { name: "Go to the first page" }))

		expect(await screen.findByText("Lead 1")).toBeInTheDocument()
		await waitFor(() => expect(router.state.location.search).toBe(""))
	})
})
