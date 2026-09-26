import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios"

import type { components } from "../types/api"
import { endSession } from "../utils/session"
import { getAccessToken, getRefreshToken, setTokens } from "../utils/token"

type TokenPair = components["schemas"]["Token"]

type RetriableRequest = InternalAxiosRequestConfig & { _retried?: boolean }

const api = axios.create({
	baseURL: import.meta.env.VITE_API_URL,
})

// Auth endpoints answer 401 for bad credentials or tokens; never refresh on them
const AUTH_PATHS = ["/auth/login/", "/auth/refresh/", "/auth/logout/"]

api.interceptors.request.use((config) => {
	const token = getAccessToken()

	if (token) {
		config.headers.Authorization = `Bearer ${token}`
	}

	return config
})

// Shared so concurrent 401s wait on a single refresh. The backend rotates
// refresh tokens, so a second parallel refresh would use a blacklisted one.
let refreshing: Promise<string> | null = null

function refreshAccessToken(): Promise<string> {
	refreshing ??= api
		.post<TokenPair>("/auth/refresh/", { refresh: getRefreshToken() })
		.then(({ data }) => {
			setTokens(data.access, data.refresh)

			return data.access
		})
		.finally(() => {
			refreshing = null
		})

	return refreshing
}

api.interceptors.response.use(undefined, async (error: AxiosError) => {
	const request = error.config as RetriableRequest | undefined

	const shouldRefresh =
		error.response?.status === 401 &&
		request !== undefined &&
		!request._retried &&
		!AUTH_PATHS.includes(request.url ?? "") &&
		getRefreshToken() !== null

	if (!shouldRefresh) {
		throw error
	}

	request._retried = true

	try {
		await refreshAccessToken()
	} catch {
		endSession()

		throw error
	}

	return api(request)
})

export default api
