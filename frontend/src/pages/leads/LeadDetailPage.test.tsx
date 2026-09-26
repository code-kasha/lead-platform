import { screen, waitFor, within } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import toast from "react-hot-toast"
import { describe, expect, it, vi } from "vitest"

import { bob, makeLead } from "../../test/fixtures"
import { fakeLeadApi } from "../../test/fakeLeadApi"
import { renderRoute } from "../../test/render"
import LeadDetailPage from "./LeadDetailPage"

vi.mock("react-hot-toast", () => ({ default: { success: vi.fn(), error: vi.fn() } }))

function card(title: string) {
	return within(screen.getByRole("heading", { name: title }).closest("section")!)
}

// Value shown next to an InfoRow label in "Lead Information"
function info(label: string) {
	return screen.getByText(label, { selector: "dt" }).nextElementSibling as HTMLElement
}

function statusOptions() {
	return within(card("Lead Status").getByRole("combobox"))
		.getAllByRole("option")
		.map((o) => o.textContent)
}

async function changeStatus(to: string) {
	await userEvent.selectOptions(card("Lead Status").getByRole("combobox"), to)
	await userEvent.click(card("Lead Status").getByRole("button", { name: "Update" }))
}

async function renderDetail() {
	renderRoute(<LeadDetailPage />, { path: "/leads/:id", url: "/leads/7" })
	await screen.findByRole("heading", { name: "Ada Lovelace" })
}

describe("LeadDetailPage status workflow", () => {
	it("offers only the transitions the backend allows", async () => {
		fakeLeadApi(makeLead({ status: "QUALIFIED" }))
		await renderDetail()

		expect(statusOptions()).toEqual(["PROPOSAL", "LOST"])
	})

	it("shows the new status right after a successful change", async () => {
		fakeLeadApi(makeLead({ status: "NEW" }))
		await renderDetail()

		await changeStatus("CONTACTED")

		await waitFor(() => expect(info("Status")).toHaveTextContent("Contacted"))
		expect(toast.success).toHaveBeenCalledWith("Lead status updated.")
	})

	it("keeps advancing through the pipeline without a page reload", async () => {
		const api = fakeLeadApi(makeLead({ status: "NEW" }))
		await renderDetail()

		await changeStatus("CONTACTED")
		await waitFor(() => expect(statusOptions()).toEqual(["QUALIFIED", "LOST"]))

		await changeStatus("QUALIFIED")
		await waitFor(() => expect(info("Status")).toHaveTextContent("Qualified"))

		expect(api.state.lead.status).toBe("QUALIFIED")
		expect(toast.error).not.toHaveBeenCalled()
	})

	it("submits the option shown after advancing, without touching the dropdown", async () => {
		const api = fakeLeadApi(makeLead({ status: "NEW" }))
		await renderDetail()

		await changeStatus("CONTACTED")
		await waitFor(() => expect(statusOptions()).toEqual(["QUALIFIED", "LOST"]))
		expect(card("Lead Status").getByRole("combobox")).toHaveValue("QUALIFIED")

		// Click Update straight away: the visible first option must be what's sent
		await userEvent.click(card("Lead Status").getByRole("button", { name: "Update" }))

		await waitFor(() => expect(api.state.lead.status).toBe("QUALIFIED"))
		expect(toast.error).not.toHaveBeenCalled()
	})

	it("disables the status control for a closed lead", async () => {
		fakeLeadApi(makeLead({ status: "WON" }))
		await renderDetail()

		expect(card("Lead Status").getByRole("combobox")).toBeDisabled()
		expect(card("Lead Status").getByRole("button", { name: "Update" })).toBeDisabled()
		expect(statusOptions()).toEqual(["No further transitions"])
	})

	it("shows the backend's reason when a change is rejected", async () => {
		const api = fakeLeadApi(makeLead({ status: "NEW" }))
		await renderDetail()
		// Someone else moves the lead on before this user clicks Update
		api.state.lead = { ...api.state.lead, status: "CONTACTED" }

		await changeStatus("CONTACTED")

		await waitFor(() => expect(toast.error).toHaveBeenCalledWith("Lead is already in this status."))
	})
})

describe("LeadDetailPage assignment", () => {
	it("shows the new assignee right after assigning", async () => {
		const api = fakeLeadApi(makeLead({ assigned_to: null }))
		await renderDetail()
		expect(info("Assigned To")).toHaveTextContent("-")

		const select = await card("Assignment").findByRole("combobox")
		await userEvent.selectOptions(select, String(bob.id))
		await userEvent.click(card("Assignment").getByRole("button", { name: "Assign" }))

		await waitFor(() => expect(info("Assigned To")).toHaveTextContent(bob.full_name))
		expect(api.post).toHaveBeenCalledWith("/leads/7/assign/", { assigned_to: bob.id })
		expect(toast.success).toHaveBeenCalledWith("Lead assigned successfully.")
	})

	it("preselects the current assignee", async () => {
		fakeLeadApi(makeLead({ assigned_to: bob }))
		await renderDetail()

		expect(await card("Assignment").findByRole("combobox")).toHaveValue(String(bob.id))
	})
})
