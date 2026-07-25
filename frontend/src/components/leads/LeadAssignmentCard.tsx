import { useEffect, useState } from "react"

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

	const [userId, setUserId] = useState<number | "">("")

	useEffect(() => {
		setUserId(currentUserId ?? "")
	}, [currentUserId])

	const { data: users, isLoading } = useQuery({
		queryKey: ["users"],
		queryFn: getUsers,
	})

	const mutation = useMutation({
		mutationFn: (assignedTo: number) => assignLead(leadId, assignedTo),

		onSuccess: () => {
			toast.success("Lead assigned successfully.")

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

		onError: () => {
			toast.error("Unable to assign lead.")
		},
	})

	return (
		<Card title="Assignment">
			<div className="flex flex-col gap-4 md:flex-row">
				<select
					className="flex-1 rounded-lg border border-gray-300 px-3 py-2"
					value={userId}
					disabled={isLoading}
					onChange={(e) =>
						setUserId(e.target.value ? Number(e.target.value) : "")
					}
				>
					<option value="">Select member</option>

					{users?.map((user) => (
						<option key={user.id} value={user.id}>
							{user.full_name}
						</option>
					))}
				</select>

				<button
					type="button"
					className="rounded-lg bg-blue-600 px-4 py-2 font-medium text-white transition hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-50"
					disabled={userId === "" || mutation.isPending}
					onClick={() => mutation.mutate(Number(userId))}
				>
					{mutation.isPending ? "Assigning..." : "Assign"}
				</button>
			</div>
		</Card>
	)
}
