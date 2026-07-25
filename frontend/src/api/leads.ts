import api from "./axios"

import type { components, paths } from "../types/api"

export type LeadCreateRequest = components["schemas"]["LeadCreateRequest"]

export type LeadUpdateRequest = components["schemas"]["LeadUpdateRequest"]

export type Lead = components["schemas"]["Lead"]

export type LeadNote = components["schemas"]["LeadNote"]

export type LeadListResponse =
	paths["/api/leads/"]["get"]["responses"]["200"]["content"]["application/json"]

export async function getLeads(): Promise<LeadListResponse> {
	const response = await api.get("/leads/")

	return response.data
}

export async function getLead(id: number): Promise<Lead> {
	const response = await api.get(`/leads/${id}/`)

	return response.data
}

export async function getLeadNotes(leadId: number): Promise<LeadNote[]> {
	const response = await api.get(`/leads/${leadId}/notes/list/`)

	return response.data
}

export async function addLeadNote(
	leadId: number,
	content: string,
): Promise<LeadNote> {
	const response = await api.post(`/leads/${leadId}/notes/`, {
		content,
	})

	return response.data
}

export async function updateLeadNote(
	noteId: number,
	content: string,
): Promise<LeadNote> {
	const response = await api.patch(`/leads/notes/${noteId}/`, {
		content,
	})

	return response.data
}

export async function deleteLeadNote(noteId: number): Promise<void> {
	await api.delete(`/leads/notes/${noteId}/`)
}

export type LeadActivity = components["schemas"]["LeadActivity"]

export async function getLeadActivities(
	leadId: number,
): Promise<LeadActivity[]> {
	const response = await api.get(`/leads/${leadId}/activities/`)

	return response.data
}

export async function createLead(data: LeadCreateRequest): Promise<Lead> {
	const response = await api.post("/leads/", data)

	return response.data
}

export async function updateLead(
	id: number,
	data: LeadUpdateRequest,
): Promise<Lead> {
	const response = await api.put(`/leads/${id}/`, data)

	return response.data
}

export async function assignLead(
	id: number,
	assigned_to: number,
): Promise<Lead> {
	const response = await api.post(`/leads/${id}/assign/`, {
		assigned_to,
	})

	return response.data
}

export async function changeLeadStatus(
	id: number,
	status: string,
): Promise<Lead> {
	const response = await api.post(`/leads/${id}/status/`, {
		status,
	})

	return response.data
}
