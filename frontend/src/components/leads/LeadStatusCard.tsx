import { useState } from "react"

import { useMutation, useQueryClient } from "@tanstack/react-query"
import toast from "react-hot-toast"

import { changeLeadStatus, type Lead } from "../../api/leads"

import Card from "../ui/Card"

import type { AxiosError } from "axios"

type Status = Lead["status"]

type Props = {
	leadId: number
	currentStatus: Status
}

const ALLOWED_TRANSITIONS: Record<Status, Status[]> = {
	NEW: ["CONTACTED", "LOST"],
	CONTACTED: ["QUALIFIED", "LOST"],
	QUALIFIED: ["PROPOSAL", "LOST"],
	PROPOSAL: ["WON", "LOST"],
	WON: [],
	LOST: [],
}

export default function LeadStatusCard({ leadId, currentStatus }: Props) {
	const queryClient = useQueryClient()

	const allowedStatuses = ALLOWED_TRANSITIONS[currentStatus]

	const [selected, setSelected] = useState<Status | null>(null)

	// Fall back to the first allowed option when the lead moves on and the
	// previous choice is no longer a valid transition
	const status =
		selected && allowedStatuses.includes(selected)
			? selected
			: (allowedStatuses[0] ?? currentStatus)

	const mutation = useMutation({
		mutationFn: () => changeLeadStatus(leadId, status),

		onSuccess: () => {
			toast.success("Lead status updated.")

			queryClient.invalidateQueries({
				queryKey: ["lead", leadId],
			})

			queryClient.invalidateQueries({
				queryKey: ["lead-activities", leadId],
			})

			queryClient.invalidateQueries({
				queryKey: ["leads"],
			})
		},

		onError: (error: AxiosError<{ status?: string }>) => {
			const message = error.response?.data?.status ?? "Unable to update status."

			toast.error(message)
		},
	})

	return (
		<Card title="Lead Status">
			<div className="flex flex-col gap-4 md:flex-row">
				<select
					className="flex-1 rounded-lg border border-gray-300 px-3 py-2"
					value={status}
					disabled={allowedStatuses.length === 0 || mutation.isPending}
					onChange={(e) => setSelected(e.target.value as Status)}
				>
					{allowedStatuses.length === 0 ? (
						<option value={currentStatus}>No further transitions</option>
					) : (
						allowedStatuses.map((item) => (
							<option key={item} value={item}>
								{item}
							</option>
						))
					)}
				</select>

				<button
					type="button"
					className="rounded-lg bg-green-600 px-4 py-2 font-medium text-white transition hover:bg-green-700 disabled:cursor-not-allowed disabled:opacity-50"
					disabled={allowedStatuses.length === 0 || mutation.isPending}
					onClick={() => mutation.mutate()}
				>
					{mutation.isPending ? "Updating..." : "Update"}
				</button>
			</div>
		</Card>
	)
}
