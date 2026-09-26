import { describe, expect, it, vi } from "vitest"

import { setTokens } from "../utils/token"
import { logout } from "./auth"
import api from "./axios"

describe("logout", () => {
	it("sends the stored refresh token so the backend can blacklist it", async () => {
		setTokens("access-1", "refresh-1")

		const post = vi.spyOn(api, "post").mockResolvedValue({ status: 205 })

		await logout()

		expect(post).toHaveBeenCalledWith("/auth/logout/", {
			refresh: "refresh-1",
		})
	})
})
