// ==============================================================================
// Test Fixtures
// ==============================================================================

import type { Lead, LeadNote } from "../api/leads"
import type { UserSummary } from "../api/users"

export const alice: UserSummary = { id: 1, full_name: "Alice Admin" }
export const bob: UserSummary = { id: 2, full_name: "Bob Member" }

export function makeLead(overrides: Partial<Lead> = {}): Lead {
	return {
		id: 7,
		first_name: "Ada",
		last_name: "Lovelace",
		email: "ada@example.com",
		phone: "",
		company: "Engines Ltd",
		source: "",
		status: "NEW",
		created_by: alice,
		assigned_to: null,
		created_at: "2026-09-01T10:00:00Z",
		updated_at: "2026-09-01T10:00:00Z",
		...overrides,
	}
}

export function makeNote(overrides: Partial<LeadNote> = {}): LeadNote {
	return {
		id: 1,
		lead: 7,
		content: "Called, left a voicemail.",
		author: alice,
		created_at: "2026-09-02T10:00:00Z",
		updated_at: "2026-09-02T10:00:00Z",
		...overrides,
	}
}
