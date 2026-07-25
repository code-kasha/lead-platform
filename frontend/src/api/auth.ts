import api from "./axios"

import type { components } from "../types/api"

export type CurrentUser = components["schemas"]["User"]

export async function login(email: string, password: string) {
	return api.post("/auth/login/", {
		email,
		password,
	})
}

export async function me(): Promise<CurrentUser> {
	const response = await api.get("/auth/me/")

	return response.data
}

export async function logout() {
	return api.post("/auth/logout/")
}
