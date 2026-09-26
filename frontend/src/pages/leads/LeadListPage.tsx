import { Link, useSearchParams } from "react-router-dom"

import { keepPreviousData, useQuery } from "@tanstack/react-query"
import { isAxiosError } from "axios"

import { getLeads } from "../../api/leads"

import Button from "../../components/ui/Button"
import Card from "../../components/ui/Card"
import PageHeader from "../../components/ui/PageHeader"
import StatusBadge from "../../components/ui/StatusBadge"

const PAGE_SIZE = 20

// ?page=N from the URL; anything missing or malformed means page 1
function parsePage(value: string | null) {
	const page = Number(value)

	return Number.isInteger(page) && page > 0 ? page : 1
}

export default function LeadListPage() {
	const [searchParams, setSearchParams] = useSearchParams()

	const page = parsePage(searchParams.get("page"))

	const { data, isLoading, isError, error } = useQuery({
		// Under ["leads"], so mutations that invalidate ["leads"] refresh every page
		queryKey: ["leads", { page }],
		queryFn: () => getLeads({ page, page_size: PAGE_SIZE }),
		// Keep the current rows on screen while the next page loads
		placeholderData: keepPreviousData,
	})

	function goToPage(next: number) {
		setSearchParams(next > 1 ? { page: String(next) } : {})
	}

	if (isLoading) {
		return (
			<div className="py-20 text-center text-gray-500">Loading leads...</div>
		)
	}

	// DRF answers 404 for a page past the end, e.g. after leads were deleted
	if (isError && isAxiosError(error) && error.response?.status === 404) {
		return (
			<div className="py-20 text-center text-gray-600">
				<p>That page doesn't exist.</p>

				<Link to="/leads" className="mt-2 inline-block text-blue-600 hover:underline">
					Go to the first page
				</Link>
			</div>
		)
	}

	if (isError || !data) {
		return (
			<div className="py-20 text-center text-red-600">
				Failed to load leads.
			</div>
		)
	}

	const firstShown = (page - 1) * PAGE_SIZE + 1
	const lastShown = firstShown + data.results.length - 1

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

				{(data.previous || data.next) && (
					<nav
						aria-label="Pagination"
						className="mt-4 flex items-center justify-between border-t border-gray-100 pt-4 text-sm text-gray-600"
					>
						<span>
							Showing {firstShown}–{lastShown} of {data.count}
						</span>

						<div className="flex gap-2">
							<Button
								variant="secondary"
								disabled={!data.previous}
								onClick={() => goToPage(page - 1)}
							>
								Previous
							</Button>

							<Button
								variant="secondary"
								disabled={!data.next}
								onClick={() => goToPage(page + 1)}
							>
								Next
							</Button>
						</div>
					</nav>
				)}
			</Card>
		</div>
	)
}
