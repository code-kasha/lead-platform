import { afterEach, describe, expect, it, vi } from "vitest"

import { endSession } from "./session"
import { getAccessToken, getRefreshToken, setTokens } from "./token"

describe("endSession", () => {
	afterEach(() => {
		vi.unstubAllGlobals()
	})

	it("clears tokens and sends the user to /login", () => {
		const assign = vi.fn()
		vi.stubGlobal("location", { pathname: "/leads", assign })
		setTokens("access-1", "refresh-1")

		endSession()

		expect(getAccessToken()).toBeNull()
		expect(getRefreshToken()).toBeNull()
		expect(assign).toHaveBeenCalledWith("/login")
	})

	it("does not reload the login page itself", () => {
		const assign = vi.fn()
		vi.stubGlobal("location", { pathname: "/login", assign })

		endSession()

		expect(assign).not.toHaveBeenCalled()
	})
})
