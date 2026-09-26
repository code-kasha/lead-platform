import { screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import type { AxiosResponse } from "axios"
import toast from "react-hot-toast"
import { describe, expect, it, vi } from "vitest"

import api from "../../api/axios"
import { makeLead } from "../../test/fixtures"
import { renderRoute } from "../../test/render"
import LeadFormPage from "./LeadFormPage"

vi.mock("react-hot-toast", () => ({ default: { success: vi.fn(), error: vi.fn() } }))

const field = (label: string) => screen.getByLabelText(label, { exact: false })

describe("LeadFormPage (create)", () => {
	function renderCreate() {
		return renderRoute(<LeadFormPage />, { path: "/leads/new", url: "/leads/new" })
	}

	it("requires first name, last name and email", async () => {
		const post = vi.spyOn(api, "post")
		renderCreate()

		await userEvent.click(screen.getByRole("button", { name: "Create Lead" }))

		expect(await screen.findByText("First name is required")).toBeInTheDocument()
		expect(screen.getByText("Last name is required")).toBeInTheDocument()
		expect(screen.getByText("Email is required")).toBeInTheDocument()
		expect(post).not.toHaveBeenCalled()
	})

	it("posts trimmed values and opens the new lead", async () => {
		const saved = makeLead({ id: 42 })
		const post = vi.spyOn(api, "post").mockResolvedValue({ data: saved } as AxiosResponse)
		const { router } = renderCreate()

		await userEvent.type(field("First Name"), "  Ada ")
		await userEvent.type(field("Last Name"), " Lovelace")
		await userEvent.type(field("Email"), "ada@example.com ")
		await userEvent.type(field("Company"), " Engines Ltd ")
		await userEvent.click(screen.getByRole("button", { name: "Create Lead" }))

		await waitFor(() => expect(router.state.location.pathname).toBe("/leads/42"))
		expect(post).toHaveBeenCalledWith("/leads/", {
			first_name: "Ada",
			last_name: "Lovelace",
			email: "ada@example.com",
			phone: "",
			company: "Engines Ltd",
			source: "",
		})
		expect(toast.success).toHaveBeenCalledWith("Lead created successfully.")
	})

	it("stays on the form and reports a failed save", async () => {
		vi.spyOn(api, "post").mockRejectedValue(new Error("400"))
		const { router } = renderCreate()

		await userEvent.type(field("First Name"), "Ada")
		await userEvent.type(field("Last Name"), "Lovelace")
		await userEvent.type(field("Email"), "ada@example.com")
		await userEvent.click(screen.getByRole("button", { name: "Create Lead" }))

		await waitFor(() => expect(toast.error).toHaveBeenCalledWith("Unable to create lead."))
		expect(router.state.location.pathname).toBe("/leads/new")
	})
})

describe("LeadFormPage (edit)", () => {
	function renderEdit() {
		return renderRoute(<LeadFormPage />, { path: "/leads/:id/edit", url: "/leads/7/edit" })
	}

	it("loads the lead into the form", async () => {
		vi.spyOn(api, "get").mockResolvedValue({ data: makeLead({ phone: "5550100" }) } as AxiosResponse)
		renderEdit()

		await waitFor(() => expect(field("First Name")).toHaveValue("Ada"))
		expect(field("Email")).toHaveValue("ada@example.com")
		expect(field("Phone")).toHaveValue("5550100")
		expect(screen.getByRole("button", { name: "Save Changes" })).toBeInTheDocument()
	})

	it("saves with PUT and caches the saved lead for the detail page", async () => {
		vi.spyOn(api, "get").mockResolvedValue({ data: makeLead() } as AxiosResponse)
		const saved = makeLead({ company: "Analytical Engines" })
		const put = vi.spyOn(api, "put").mockResolvedValue({ data: saved } as AxiosResponse)
		const { router, queryClient } = renderEdit()

		await waitFor(() => expect(field("Company")).toHaveValue("Engines Ltd"))
		await userEvent.clear(field("Company"))
		await userEvent.type(field("Company"), "Analytical Engines")
		await userEvent.click(screen.getByRole("button", { name: "Save Changes" }))

		await waitFor(() => expect(router.state.location.pathname).toBe("/leads/7"))
		expect(put).toHaveBeenCalledWith("/leads/7/", expect.objectContaining({ company: "Analytical Engines" }))
		// The detail page reads ["lead", 7]; it must not show the pre-edit data
		expect(queryClient.getQueryData(["lead", 7])).toEqual(saved)
	})
})
