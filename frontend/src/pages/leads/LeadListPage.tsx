import { Link } from "react-router-dom"

import { useQuery } from "@tanstack/react-query"

import { getLeads } from "../../api/leads"
import type { Lead } from "../../types"

export default function LeadListPage() {
	const { data, isLoading } = useQuery({
		queryKey: ["leads"],
		queryFn: getLeads,
	})

	if (isLoading) {
		return <div className="py-20 text-center">Loading leads...</div>
	}

	if (!data?.results.length) {
		return (
			<div className="rounded-lg border bg-white p-12 text-center">
				<h2 className="text-xl font-semibold">No leads found</h2>

				<p className="mt-2 text-gray-500">Create your first lead.</p>
			</div>
		)
	}

	return (
		<div>
			<div className="mb-6 flex items-center justify-between">
				<h1 className="text-3xl font-bold">Leads</h1>

				<Link
					to="/leads/new"
					className="rounded bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
				>
					New Lead
				</Link>
			</div>

			<div className="overflow-hidden rounded-lg border bg-white shadow-sm">
				<table className="w-full">
					<thead className="bg-slate-100">
						<tr>
							<th className="px-4 py-3 text-left">Name</th>

							<th className="px-4 py-3 text-left">Email</th>

							<th className="px-4 py-3 text-left">Status</th>

							<th className="px-4 py-3 text-left">Assigned To</th>
						</tr>
					</thead>

					<tbody>
						{data.results.map((lead: Lead) => (
							<tr key={lead.id} className="hover:bg-slate-50">
								<td className="border-t px-4 py-3">
									<Link
										to={`/leads/${lead.id}`}
										className="font-medium text-blue-600 hover:underline"
									>
										{lead.first_name} {lead.last_name}
									</Link>
								</td>

								<td className="border-t px-4 py-3">{lead.email}</td>

								<td className="border-t px-4 py-3">
									<span className="rounded bg-blue-100 px-2 py-1 text-sm font-medium text-blue-700">
										{lead.status}
									</span>
								</td>

								<td className="border-t px-4 py-3">
									{lead.assigned_to
										? `${lead.assigned_to.first_name} ${lead.assigned_to.last_name}`
										: "-"}
								</td>
							</tr>
						))}
					</tbody>
				</table>
			</div>
		</div>
	)
}
