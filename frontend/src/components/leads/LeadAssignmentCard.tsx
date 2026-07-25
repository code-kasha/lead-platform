// ==============================================================================
// Lead Assignment Card
// ==============================================================================

import { useState } from "react"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import toast from "react-hot-toast"

import { assignLead } from "../../api/leads"
import { getUsers } from "../../api/users"

import Button from "../ui/Button"
import Card from "../ui/Card"
import Spinner from "../ui/Spinner"

type Props = {
	leadId: number
	currentUserId?: number | null
}

export default function LeadAssignmentCard({ leadId, currentUserId }: Props) {
	const queryClient = useQueryClient()

	const [selectedUserId, setSelectedUserId] = useState<number | null>(null)

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

	const value = selectedUserId ?? currentUserId ?? ""

	return (
		<Card title="Assignment" subtitle="Assign this lead to a team member.">
			{isLoading ? (
				<Spinner label="Loading users..." />
			) : (
				<div className="flex flex-col gap-4 md:flex-row">
					<select
						className="flex-1 rounded-lg border border-gray-300 px-3 py-2 focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
						value={value}
						onChange={(e) =>
							setSelectedUserId(e.target.value ? Number(e.target.value) : null)
						}
					>
						<option value="">Select member</option>

						{users?.map((user) => (
							<option key={user.id} value={user.id}>
								{user.full_name}
							</option>
						))}
					</select>

					<Button
						loading={mutation.isPending}
						disabled={value === ""}
						onClick={() => mutation.mutate(Number(value))}
					>
						Assign
					</Button>
				</div>
			)}
		</Card>
	)
}
