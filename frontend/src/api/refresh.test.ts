import {
	AxiosError,
	type AxiosAdapter,
	type AxiosResponse,
	type InternalAxiosRequestConfig,
} from "axios"
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"

import { endSession } from "../utils/session"
import { getAccessToken, getRefreshToken, setTokens } from "../utils/token"
import api from "./axios"

vi.mock("../utils/session", () => ({ endSession: vi.fn() }))

type Handler = (config: InternalAxiosRequestConfig) => [number, unknown]

// Minimal fake backend: routes each request through `handler` and rejects
// non-2xx responses the way axios's real adapters do
function fakeServer(handler: Handler) {
	const calls: string[] = []

	const adapter: AxiosAdapter = async (config) => {
		calls.push(`${config.url} ${config.headers.Authorization ?? "-"}`)

		const [status, data] = handler(config)
		const response: AxiosResponse = { data, status, statusText: "", headers: {}, config }

		if (status >= 400) {
			throw new AxiosError("fail", undefined, config, undefined, response)
		}

		return response
	}

	api.defaults.adapter = adapter

	return calls
}

// A backend where only `validAccess` is accepted and `validRefresh` rotates
const backend =
	(validAccess: string, validRefresh: string | null): Handler =>
	(config) => {
		if (config.url === "/auth/refresh/") {
			const { refresh } = JSON.parse(config.data)

			return refresh === validRefresh
				? [200, { access: "access-2", refresh: "refresh-2" }]
				: [401, { detail: "Token is blacklisted" }]
		}

		return config.headers.Authorization === `Bearer ${validAccess}`
			? [200, { ok: true }]
			: [401, { detail: "Token expired" }]
	}

const originalAdapter = api.defaults.adapter

beforeEach(() => {
	vi.mocked(endSession).mockClear()
})

afterEach(() => {
	api.defaults.adapter = originalAdapter
})

describe("expired access token", () => {
	it("refreshes once, stores the rotated pair and retries the request", async () => {
		setTokens("access-1", "refresh-1")
		const calls = fakeServer(backend("access-2", "refresh-1"))

		const response = await api.get("/leads/")

		expect(response.data).toEqual({ ok: true })
		expect(calls).toEqual([
			"/leads/ Bearer access-1",
			"/auth/refresh/ Bearer access-1",
			"/leads/ Bearer access-2",
		])
		expect(getAccessToken()).toBe("access-2")
		expect(getRefreshToken()).toBe("refresh-2")
		expect(endSession).not.toHaveBeenCalled()
	})

	it("shares one refresh between concurrent requests", async () => {
		setTokens("access-1", "refresh-1")
		const calls = fakeServer(backend("access-2", "refresh-1"))

		await Promise.all([api.get("/leads/"), api.get("/auth/me/"), api.get("/auth/users/")])

		expect(calls.filter((c) => c.startsWith("/auth/refresh/"))).toHaveLength(1)
	})

	it("ends the session when the refresh token is rejected", async () => {
		setTokens("access-1", "refresh-stale")
		fakeServer(backend("access-2", "refresh-1"))

		await expect(api.get("/leads/")).rejects.toMatchObject({
			response: { status: 401 },
		})
		expect(endSession).toHaveBeenCalledOnce()
	})

	it("does not retry a request that still fails after refreshing", async () => {
		setTokens("access-1", "refresh-1")
		// Refresh succeeds, but the new token is still refused
		const calls = fakeServer(backend("never-valid", "refresh-1"))

		await expect(api.get("/leads/")).rejects.toMatchObject({
			response: { status: 401 },
		})
		expect(calls).toHaveLength(3)
	})
})

describe("requests that must not trigger a refresh", () => {
	it("passes a failed login straight through", async () => {
		const calls = fakeServer(() => [401, { detail: "No active account" }])

		await expect(api.post("/auth/login/", {})).rejects.toMatchObject({
			response: { status: 401 },
		})
		expect(calls).toHaveLength(1)
		expect(endSession).not.toHaveBeenCalled()
	})

	it("passes a 401 through when there is no refresh token", async () => {
		const calls = fakeServer(() => [401, { detail: "Not authenticated" }])

		await expect(api.get("/leads/")).rejects.toMatchObject({
			response: { status: 401 },
		})
		expect(calls).toHaveLength(1)
	})

	it("passes other errors straight through", async () => {
		setTokens("access-1", "refresh-1")
		const calls = fakeServer(() => [403, { detail: "Forbidden" }])

		await expect(api.get("/leads/")).rejects.toMatchObject({
			response: { status: 403 },
		})
		expect(calls).toHaveLength(1)
	})
})
