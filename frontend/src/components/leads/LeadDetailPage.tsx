import { Link, useParams } from "react-router-dom"

import { useQuery } from "@tanstack/react-query"

import { getLead } from "../../api/leads"

import LeadActivities from "../../components/leads/LeadActivities"
import LeadNotes from "../../components/leads/LeadNotes"
import Card from "../../components/ui/Card"
import InfoRow from "../../components/ui/InfoRow"
import PageHeader from "../../components/ui/PageHeader"
import StatusBadge from "../../components/ui/StatusBadge"
import LeadAssignmentCard from "../../components/leads/LeadAssignmentCard"

export default function LeadDetailPage() {
	const { id } = useParams()

	const {
		data: lead,
		isLoading,
		isError,
	} = useQuery({
		queryKey: ["lead", id],
		queryFn: () => getLead(Number(id)),
	})

	if (isLoading) {
		return <div className="py-20 text-center">Loading lead...</div>
	}

	if (isError || !lead) {
		return <div className="py-20 text-center">Lead not found.</div>
	}

	return (
		<div className="space-y-6">
			<PageHeader
				title={`${lead.first_name} ${lead.last_name}`}
				description="Lead information"
				action={
					<Link
						to={`/leads/${lead.id}/edit`}
						className="rounded-lg bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700"
					>
						Edit Lead
					</Link>
				}
			/>

			<Card title="Lead Information">
				<dl className="grid grid-cols-1 gap-6 md:grid-cols-2">
					<InfoRow label="Email" value={lead.email} />

					<InfoRow label="Phone" value={lead.phone || "-"} />

					<InfoRow label="Company" value={lead.company || "-"} />

					<InfoRow label="Source" value={lead.source || "-"} />

					<InfoRow
						label="Status"
						value={<StatusBadge status={lead.status} />}
					/>

					<InfoRow
						label="Assigned To"
						value={lead.assigned_to ? lead.assigned_to.full_name : "-"}
					/>

					<InfoRow
						label="Created By"
						value={lead.created_by ? lead.created_by.full_name : "-"}
					/>

					<InfoRow
						label="Created"
						value={new Date(lead.created_at).toLocaleString()}
					/>

					<InfoRow
						label="Last Updated"
						value={new Date(lead.updated_at).toLocaleString()}
					/>
				</dl>
			</Card>
			<LeadAssignmentCard
				leadId={lead.id}
				currentUserId={lead.assigned_to?.id}
			/>
			<LeadNotes leadId={lead.id} />

			<LeadActivities leadId={lead.id} />
		</div>
	)
}
