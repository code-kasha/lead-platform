import { AxiosError, type AxiosResponse } from "axios"
import { describe, expect, it } from "vitest"

import { shouldRetry } from "./query"

function httpError(status: number) {
	return new AxiosError("fail", undefined, undefined, undefined, { status } as AxiosResponse)
}

describe("query retry policy", () => {
	it.each([400, 403, 404])("does not retry a %i", (status) => {
		expect(shouldRetry(0, httpError(status))).toBe(false)
	})

	it("retries a server error once", () => {
		expect(shouldRetry(0, httpError(503))).toBe(true)
		expect(shouldRetry(1, httpError(503))).toBe(false)
	})

	it("retries a network failure once", () => {
		expect(shouldRetry(0, new AxiosError("Network Error"))).toBe(true)
		expect(shouldRetry(1, new AxiosError("Network Error"))).toBe(false)
	})
})
