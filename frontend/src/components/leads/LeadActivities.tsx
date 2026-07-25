import { useQuery } from "@tanstack/react-query"

import { getLeadActivities } from "../../api/leads"

import Card from "../ui/Card"

type Props = {
	leadId: number
}

export default function LeadActivities({ leadId }: Props) {
	const {
		data: activities,
		isLoading,
		isError,
	} = useQuery({
		queryKey: ["lead-activities", leadId],
		queryFn: () => getLeadActivities(leadId),
	})

	return (
		<Card title="Activity Timeline">
			{isLoading && <p>Loading activities...</p>}

			{isError && <p className="text-red-600">Failed to load activities.</p>}

			{!isLoading && !isError && activities?.length === 0 && (
				<p className="text-gray-500">No activity recorded.</p>
			)}

			<div className="space-y-4">
				{activities?.map((activity) => (
					<div key={activity.id} className="rounded-lg border p-4">
						<div className="flex items-center justify-between">
							<span className="font-semibold">
								{activity.activity_type
									.replaceAll("_", " ")
									.toLowerCase()
									.replace(/\b\w/g, (c) => c.toUpperCase())}
							</span>

							<span className="text-sm text-gray-500">
								{new Date(activity.created_at).toLocaleString()}
							</span>
						</div>

						<p className="mt-2">{activity.description}</p>

						<div className="mt-3 text-sm text-gray-500">
							{activity.user.full_name}
						</div>
					</div>
				))}
			</div>
		</Card>
	)
}
