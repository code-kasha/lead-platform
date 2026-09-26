import { screen, waitFor, within } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import toast from "react-hot-toast"
import { describe, expect, it, vi } from "vitest"

import { makeLead, makeNote } from "../../test/fixtures"
import { fakeLeadApi } from "../../test/fakeLeadApi"
import { renderRoute } from "../../test/render"
import LeadNotes from "./LeadNotes"

vi.mock("react-hot-toast", () => ({ default: { success: vi.fn(), error: vi.fn() } }))

function renderNotes() {
	renderRoute(<LeadNotes leadId={7} />, { path: "/leads/:id", url: "/leads/7" })
}

// The card holding a note's text
function noteCard(text: string) {
	return within(screen.getByText(text).closest("div.rounded-xl") as HTMLElement)
}

describe("LeadNotes", () => {
	it("shows an empty state when there are no notes", async () => {
		fakeLeadApi(makeLead())
		renderNotes()

		expect(await screen.findByText("No Notes")).toBeInTheDocument()
	})

	it("lists notes with their author", async () => {
		fakeLeadApi(makeLead(), [makeNote({ content: "Sent the proposal." })])
		renderNotes()

		expect(await screen.findByText("Sent the proposal.")).toBeInTheDocument()
		expect(noteCard("Sent the proposal.").getByText("Alice Admin")).toBeInTheDocument()
	})

	it("adds a trimmed note, clears the box and shows it", async () => {
		const api = fakeLeadApi(makeLead())
		renderNotes()
		await screen.findByText("No Notes")

		const addButton = screen.getByRole("button", { name: "Add Note" })
		expect(addButton).toBeDisabled()

		await userEvent.type(screen.getByPlaceholderText("Write a note..."), "  Follow up Friday  ")
		await userEvent.click(addButton)

		expect(await screen.findByText("Follow up Friday")).toBeInTheDocument()
		expect(api.post).toHaveBeenCalledWith("/leads/7/notes/", { content: "Follow up Friday" })
		expect(screen.getByPlaceholderText("Write a note...")).toHaveValue("")
		expect(toast.success).toHaveBeenCalledWith("Note added.")
	})

	it("does not allow a whitespace-only note", async () => {
		fakeLeadApi(makeLead())
		renderNotes()
		await screen.findByText("No Notes")

		await userEvent.type(screen.getByPlaceholderText("Write a note..."), "   ")

		expect(screen.getByRole("button", { name: "Add Note" })).toBeDisabled()
	})

	it("edits a note in place", async () => {
		const api = fakeLeadApi(makeLead(), [makeNote({ id: 3, content: "Old text" })])
		renderNotes()
		await screen.findByText("Old text")

		await userEvent.click(noteCard("Old text").getByRole("button", { name: "Edit" }))
		const box = screen.getByDisplayValue("Old text")
		await userEvent.clear(box)
		await userEvent.type(box, " New text ")
		await userEvent.click(screen.getByRole("button", { name: "Save" }))

		expect(await screen.findByText("New text")).toBeInTheDocument()
		expect(api.patch).toHaveBeenCalledWith("/leads/notes/3/", { content: "New text" })
		expect(screen.queryByText("Old text")).not.toBeInTheDocument()
	})

	it("cancels an edit without saving", async () => {
		const api = fakeLeadApi(makeLead(), [makeNote({ content: "Keep me" })])
		renderNotes()
		await screen.findByText("Keep me")

		await userEvent.click(noteCard("Keep me").getByRole("button", { name: "Edit" }))
		await userEvent.type(screen.getByDisplayValue("Keep me"), " changed")
		await userEvent.click(screen.getByRole("button", { name: "Cancel" }))

		expect(screen.getByText("Keep me")).toBeInTheDocument()
		expect(api.patch).not.toHaveBeenCalled()
	})

	it("deletes a note", async () => {
		const api = fakeLeadApi(makeLead(), [makeNote({ id: 5, content: "Delete me" })])
		renderNotes()
		await screen.findByText("Delete me")

		await userEvent.click(noteCard("Delete me").getByRole("button", { name: "Delete" }))

		await waitFor(() => expect(screen.queryByText("Delete me")).not.toBeInTheDocument())
		expect(api.delete).toHaveBeenCalledWith("/leads/notes/5/")
		expect(await screen.findByText("No Notes")).toBeInTheDocument()
	})
})
