import { render, screen } from "@testing-library/react"
import { describe, expect, it } from "vitest"

import StatusBadge from "./StatusBadge"

describe("StatusBadge", () => {
	it.each([
		["NEW", "New"],
		["CONTACTED", "Contacted"],
		["QUALIFIED", "Qualified"],
		["PROPOSAL", "Proposal"],
		["WON", "Won"],
		["LOST", "Lost"],
	])("labels %s as %s", (status, label) => {
		render(<StatusBadge status={status} />)

		expect(screen.getByText(label)).toBeInTheDocument()
	})

	it("falls back to the raw value for an unknown status", () => {
		render(<StatusBadge status="ARCHIVED" />)

		expect(screen.getByText("ARCHIVED")).toHaveClass("bg-gray-100")
	})
})
