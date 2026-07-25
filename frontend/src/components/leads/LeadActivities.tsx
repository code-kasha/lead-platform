// ==============================================================================
// Lead Activities
// ==============================================================================

import { useQuery } from "@tanstack/react-query"

import { getLeadActivities } from "../../api/leads"

import Card from "../ui/Card"
import EmptyState from "../ui/EmptyState"
import Spinner from "../ui/Spinner"

type Props = {
	leadId: number
}

function formatActivityType(activityType: string) {
	return activityType
		.replaceAll("_", " ")
		.toLowerCase()
		.replace(/\b\w/g, (char) => char.toUpperCase())
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
		<Card
			title="Activity Timeline"
			subtitle="Recent actions performed on this lead."
		>
			{isLoading && <Spinner label="Loading activities..." />}

			{isError && (
				<div className="rounded-lg border border-red-200 bg-red-50 p-4 text-red-700">
					Unable to load activities.
				</div>
			)}

			{!isLoading && !isError && activities?.length === 0 && (
				<EmptyState
					title="No Activities"
					description="No activity has been recorded for this lead."
				/>
			)}

			<div className="space-y-4">
				{activities?.map((activity) => (
					<div
						key={activity.id}
						className="rounded-xl border border-gray-200 bg-white p-5 shadow-sm transition hover:shadow-md"
					>
						<div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
							<h3 className="text-sm font-semibold tracking-wide text-gray-900">
								{formatActivityType(activity.activity_type)}
							</h3>

							<span className="text-sm text-gray-500">
								{new Date(activity.created_at).toLocaleString()}
							</span>
						</div>

						<p className="mt-3 leading-7 text-gray-700">
							{activity.description}
						</p>

						<div className="mt-4 flex items-center justify-between border-t border-gray-100 pt-3 text-sm text-gray-500">
							<span>{activity.user.full_name}</span>

							<span>ID #{activity.id}</span>
						</div>
					</div>
				))}
			</div>
		</Card>
	)
}
