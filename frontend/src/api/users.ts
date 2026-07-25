import api from "./axios"

import type { components, paths } from "../types/api"

export type UserSummary = components["schemas"]["UserSummary"]

export type UserListResponse =
	paths["/api/auth/users/"]["get"]["responses"]["200"]["content"]["application/json"]

export async function getUsers(): Promise<UserSummary[]> {
	const response = await api.get("/auth/users/")

	return response.data.results ?? response.data
}
