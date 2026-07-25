import { ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY } from "../constants/storage"

export function getAccessToken() {
	return localStorage.getItem(ACCESS_TOKEN_KEY)
}

export function getRefreshToken() {
	return localStorage.getItem(REFRESH_TOKEN_KEY)
}

export function setTokens(access: string, refresh: string) {
	localStorage.setItem(ACCESS_TOKEN_KEY, access)

	localStorage.setItem(REFRESH_TOKEN_KEY, refresh)
}

export function clearTokens() {
	localStorage.removeItem(ACCESS_TOKEN_KEY)
	localStorage.removeItem(REFRESH_TOKEN_KEY)
}
