import { Link } from "react-router-dom"

import { useQuery } from "@tanstack/react-query"

import { getLeads } from "../../api/leads"

import Card from "../../components/ui/Card"
import PageHeader from "../../components/ui/PageHeader"
import StatusBadge from "../../components/ui/StatusBadge"

export default function LeadListPage() {
	const { data, isLoading, isError } = useQuery({
		queryKey: ["leads"],
		queryFn: getLeads,
	})

	if (isLoading) {
		return (
			<div className="py-20 text-center text-gray-500">Loading leads...</div>
		)
	}

	if (isError || !data) {
		return (
			<div className="py-20 text-center text-red-600">
				Failed to load leads.
			</div>
		)
	}

	return (
		<div className="space-y-6">
			<PageHeader
				title="Leads"
				description="Manage your sales pipeline."
				action={
					<Link
						to="/leads/new"
						className="rounded-lg bg-blue-600 px-4 py-2 text-white transition hover:bg-blue-700"
					>
						New Lead
					</Link>
				}
			/>

			<Card>
				<div className="overflow-x-auto">
					<table className="min-w-full divide-y divide-gray-200">
						<thead className="bg-gray-50">
							<tr>
								<th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
									Name
								</th>

								<th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
									Company
								</th>

								<th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
									Email
								</th>

								<th className="px-6 py-3 text-left text-xs font-semibold uppercase tracking-wide text-gray-500">
									Status
								</th>

								<th className="px-6 py-3 text-right text-xs font-semibold uppercase tracking-wide text-gray-500">
									Actions
								</th>
							</tr>
						</thead>

						<tbody className="divide-y divide-gray-200 bg-white">
							{data.results.map((lead) => (
								<tr key={lead.id} className="hover:bg-gray-50">
									<td className="px-6 py-4 font-medium text-gray-900">
										{lead.first_name} {lead.last_name}
									</td>

									<td className="px-6 py-4 text-gray-700">
										{lead.company || "-"}
									</td>

									<td className="px-6 py-4 text-gray-700">{lead.email}</td>

									<td className="px-6 py-4">
										<StatusBadge status={lead.status} />
									</td>

									<td className="px-6 py-4 text-right">
										<Link
											to={`/leads/${lead.id}`}
											className="font-medium text-blue-600 hover:text-blue-700"
										>
											View
										</Link>
									</td>
								</tr>
							))}
						</tbody>
					</table>

					{data.results.length === 0 && (
						<div className="py-12 text-center text-gray-500">
							No leads found.
						</div>
					)}
				</div>
			</Card>
		</div>
	)
}
