import type { AxiosAdapter } from "axios"
import { describe, expect, it } from "vitest"

import { setTokens } from "../utils/token"
import api from "./axios"

// Echo the outgoing request back instead of sending it
const echo: AxiosAdapter = async (config) => ({
	data: {
		url: config.url,
		baseURL: config.baseURL,
		authorization: config.headers.Authorization ?? null,
	},
	status: 200,
	statusText: "OK",
	headers: {},
	config,
})

describe("api client", () => {
	it("uses VITE_API_URL as its base URL", async () => {
		const response = await api.get("/leads/", { adapter: echo })

		expect(response.data.baseURL).toBe("http://api.test/api")
	})

	it("sends no Authorization header when logged out", async () => {
		const response = await api.get("/leads/", { adapter: echo })

		expect(response.data.authorization).toBeNull()
	})

	it("attaches the stored access token as a Bearer header", async () => {
		setTokens("access-1", "refresh-1")

		const response = await api.get("/leads/", { adapter: echo })

		expect(response.data.authorization).toBe("Bearer access-1")
	})
})
