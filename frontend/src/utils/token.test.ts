import { describe, expect, it } from "vitest"

import { ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY } from "../constants/storage"
import {
	clearTokens,
	getAccessToken,
	getRefreshToken,
	setTokens,
} from "./token"

describe("token storage", () => {
	it("returns null when no tokens are stored", () => {
		expect(getAccessToken()).toBeNull()
		expect(getRefreshToken()).toBeNull()
	})

	it("stores both tokens under their storage keys", () => {
		setTokens("access-1", "refresh-1")

		expect(getAccessToken()).toBe("access-1")
		expect(getRefreshToken()).toBe("refresh-1")
		expect(localStorage.getItem(ACCESS_TOKEN_KEY)).toBe("access-1")
		expect(localStorage.getItem(REFRESH_TOKEN_KEY)).toBe("refresh-1")
	})

	it("clears both tokens", () => {
		setTokens("access-1", "refresh-1")

		clearTokens()

		expect(getAccessToken()).toBeNull()
		expect(getRefreshToken()).toBeNull()
	})
})
