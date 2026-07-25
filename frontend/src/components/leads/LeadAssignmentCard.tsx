import { useState } from "react"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import toast from "react-hot-toast"

import { assignLead } from "../../api/leads"
import { getUsers } from "../../api/users"

import Card from "../ui/Card"

type Props = {
	leadId: number
	currentUserId?: number | null
}

export default function LeadAssignmentCard({ leadId, currentUserId }: Props) {
	const queryClient = useQueryClient()

	const [userId, setUserId] = useState<number | "">(currentUserId ?? "")

	const { data: users } = useQuery({
		queryKey: ["users"],
		queryFn: getUsers,
	})

	const mutation = useMutation({
		mutationFn: (assignedTo: number) => assignLead(leadId, assignedTo),

		onSuccess: () => {
			toast.success("Lead assigned.")

			queryClient.invalidateQueries({
				queryKey: ["lead", leadId],
			})

			queryClient.invalidateQueries({
				queryKey: ["lead-activities", leadId],
			})
		},

		onError: () => {
			toast.error("Unable to assign lead.")
		},
	})

	return (
		<Card title="Assignment">
			<div className="flex gap-4">
				<select
					className="flex-1 rounded border px-3 py-2"
					value={userId}
					onChange={(e) => setUserId(Number(e.target.value))}
				>
					<option value="">Select member</option>

					{users?.map((user) => (
						<option key={user.id} value={user.id}>
							{user.full_name}
						</option>
					))}
				</select>

				<button
					className="rounded bg-blue-600 px-4 py-2 text-white disabled:opacity-50"
					disabled={userId === "" || mutation.isPending}
					onClick={() => mutation.mutate(Number(userId))}
				>
					Assign
				</button>
			</div>
		</Card>
	)
}
