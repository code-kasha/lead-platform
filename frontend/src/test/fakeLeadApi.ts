// ==============================================================================
// Fake Lead API
// ==============================================================================

import { AxiosError, type AxiosResponse } from "axios"
import { vi } from "vitest"

import api from "../api/axios"
import type { Lead, LeadNote } from "../api/leads"
import { alice, bob } from "./fixtures"

// Mirrors backend/apps/leads/constants.py so the fake rejects what the API rejects
const TRANSITIONS: Record<Lead["status"], Lead["status"][]> = {
	NEW: ["CONTACTED", "LOST"],
	CONTACTED: ["QUALIFIED", "LOST"],
	QUALIFIED: ["PROPOSAL", "LOST"],
	PROPOSAL: ["WON", "LOST"],
	WON: [],
	LOST: [],
}

function reply(data: unknown) {
	return Promise.resolve({ data } as AxiosResponse)
}

function fail(status: number, data: unknown) {
	return Promise.reject(
		new AxiosError("Request failed", undefined, undefined, undefined, {
			status,
			data,
		} as AxiosResponse),
	)
}

// Stateful stand-in for one lead's endpoints, backed by vi.spyOn on the api client
export function fakeLeadApi(initial: Lead, initialNotes: LeadNote[] = []) {
	const state = { lead: { ...initial }, notes: [...initialNotes] }
	const base = `/leads/${initial.id}/`
	let nextNoteId = 100

	const get = vi.spyOn(api, "get").mockImplementation((url: string) => {
		if (url === base) return reply(state.lead)
		if (url === `${base}notes/list/`) return reply(state.notes)
		if (url === `${base}activities/`) return reply([])
		if (url === "/auth/users/") return reply([alice, bob])
		if (url === "/leads/") return reply({ count: 1, results: [state.lead] })
		return fail(404, { detail: "Not found." })
	})

	const post = vi.spyOn(api, "post").mockImplementation((url: string, body?: unknown) => {
		const data = body as Record<string, unknown>

		if (url === `${base}status/`) {
			const next = data.status as Lead["status"]

			if (next === state.lead.status) {
				return fail(400, { status: "Lead is already in this status." })
			}
			if (!TRANSITIONS[state.lead.status].includes(next)) {
				return fail(400, { status: `Cannot change status from ${state.lead.status} to ${next}.` })
			}
			state.lead = { ...state.lead, status: next }
			return reply(state.lead)
		}

		if (url === `${base}assign/`) {
			const user = [alice, bob].find((u) => u.id === data.assigned_to) ?? null
			state.lead = { ...state.lead, assigned_to: user }
			return reply(state.lead)
		}

		if (url === `${base}notes/`) {
			const note: LeadNote = {
				id: nextNoteId++,
				lead: initial.id,
				content: data.content as string,
				author: alice,
				created_at: "2026-09-03T10:00:00Z",
				updated_at: "2026-09-03T10:00:00Z",
			}
			state.notes = [note, ...state.notes]
			return reply(note)
		}

		return fail(404, { detail: "Not found." })
	})

	const patch = vi.spyOn(api, "patch").mockImplementation((url: string, body?: unknown) => {
		const match = url.match(/^\/leads\/notes\/(\d+)\/$/)
		const note = match && state.notes.find((n) => n.id === Number(match[1]))
		if (!note) return fail(404, { detail: "Not found." })

		const updated = { ...note, content: (body as { content: string }).content }
		state.notes = state.notes.map((n) => (n.id === note.id ? updated : n))
		return reply(updated)
	})

	const del = vi.spyOn(api, "delete").mockImplementation((url: string) => {
		const match = url.match(/^\/leads\/notes\/(\d+)\/$/)
		if (!match) return fail(404, { detail: "Not found." })

		state.notes = state.notes.filter((n) => n.id !== Number(match[1]))
		return reply(undefined)
	})

	return { state, get, post, patch, delete: del }
}
