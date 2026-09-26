import api from "./axios"

import { getRefreshToken } from "../utils/token"

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
	// The backend blacklists the submitted refresh token
	return api.post("/auth/logout/", {
		refresh: getRefreshToken(),
	})
}
