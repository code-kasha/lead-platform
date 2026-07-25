// ==============================================================================
// Lead Detail Page
// ==============================================================================

import { Link, useParams } from "react-router-dom"

import { useQuery } from "@tanstack/react-query"

import { getLead } from "../../api/leads"

import LeadActivities from "../../components/leads/LeadActivities"
import LeadAssignmentCard from "../../components/leads/LeadAssignmentCard"
import LeadNotes from "../../components/leads/LeadNotes"
import LeadStatusCard from "../../components/leads/LeadStatusCard"

import Button from "../../components/ui/Button"
import Card from "../../components/ui/Card"
import InfoRow from "../../components/ui/InfoRow"
import PageHeader from "../../components/ui/PageHeader"
import Spinner from "../../components/ui/Spinner"
import StatusBadge from "../../components/ui/StatusBadge"

export default function LeadDetailPage() {
	const { id } = useParams()

	const {
		data: lead,
		isLoading,
		isError,
	} = useQuery({
		queryKey: ["lead", id],
		queryFn: () => getLead(Number(id)),
		enabled: !!id,
	})

	if (isLoading) {
		return <Spinner label="Loading lead..." />
	}

	if (isError || !lead) {
		return <div className="py-20 text-center text-red-600">Lead not found.</div>
	}

	return (
		<div className="space-y-6">
			<PageHeader
				title={`${lead.first_name} ${lead.last_name}`}
				description="Lead information"
				action={
					<Link to={`/leads/${lead.id}/edit`}>
						<Button>Edit Lead</Button>
					</Link>
				}
			/>

			<Card title="Lead Information">
				<div className="grid grid-cols-1 gap-6 md:grid-cols-2">
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
						value={lead.assigned_to?.full_name ?? "-"}
					/>

					<InfoRow
						label="Created By"
						value={lead.created_by?.full_name ?? "-"}
					/>

					<InfoRow
						label="Created"
						value={new Date(lead.created_at).toLocaleString()}
					/>

					<InfoRow
						label="Updated"
						value={new Date(lead.updated_at).toLocaleString()}
					/>
				</div>
			</Card>

			<LeadStatusCard leadId={lead.id} currentStatus={lead.status} />

			<LeadAssignmentCard
				leadId={lead.id}
				currentUserId={lead.assigned_to?.id ?? null}
			/>

			<LeadNotes leadId={lead.id} />

			<LeadActivities leadId={lead.id} />
		</div>
	)
}
