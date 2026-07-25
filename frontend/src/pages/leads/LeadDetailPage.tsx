import { useParams } from "react-router-dom"

import { useQuery } from "@tanstack/react-query"

import { getLead } from "../../api/leads"

import Card from "../../components/ui/Card"
import InfoRow from "../../components/ui/InfoRow"
import PageHeader from "../../components/ui/PageHeader"
import StatusBadge from "../../components/ui/StatusBadge"
import LeadNotes from "../../components/leads/LeadNotes"
import LeadActivities from "../../components/leads/LeadActivities"

export default function LeadDetailPage() {
	const { id } = useParams()

	const { data, isLoading } = useQuery({
		queryKey: ["lead", id],
		queryFn: () => getLead(Number(id)),
	})

	if (isLoading) {
		return <div className="py-20 text-center">Loading lead...</div>
	}

	if (!data) {
		return <div className="py-20 text-center">Lead not found.</div>
	}

	return (
		<div className="space-y-6">
			<PageHeader
				title={`${data.first_name} ${data.last_name}`}
				description="Lead information"
			/>

			<Card>
				<dl className="grid grid-cols-1 gap-6 md:grid-cols-2">
					<InfoRow label="Email" value={data.email} />

					<InfoRow label="Phone" value={data.phone || "-"} />

					<InfoRow label="Company" value={data.company || "-"} />

					<InfoRow label="Source" value={data.source || "-"} />

					<InfoRow
						label="Status"
						value={<StatusBadge status={data.status} />}
					/>

					<InfoRow
						label="Assigned To"
						value={data.assigned_to?.full_name ?? "-"}
					/>

					<InfoRow
						label="Created By"
						value={data.created_by?.full_name ?? "-"}
					/>

					<InfoRow
						label="Created"
						value={new Date(data.created_at).toLocaleString()}
					/>

					<InfoRow
						label="Last Updated"
						value={new Date(data.updated_at).toLocaleString()}
					/>
				</dl>
			</Card>
			<LeadNotes leadId={data.id} />
			<LeadActivities leadId={data.id} />
		</div>
	)
}
