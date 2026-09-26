import { Link } from "react-router-dom"

import Card from "../../components/ui/Card"
import PageHeader from "../../components/ui/PageHeader"

export default function DashboardPage() {
	return (
		<div className="space-y-6">
			<PageHeader title="Dashboard" description="Lead Management Platform" />

			<div className="grid gap-6 md:grid-cols-3">
				<Card title="Leads">
					<div className="space-y-4">
						<p className="text-sm text-gray-600">
							View, create and manage your leads.
						</p>

						<Link
							to="/leads"
							className="inline-flex rounded-lg bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
						>
							View Leads
						</Link>
					</div>
				</Card>

				<Card title="Create Lead">
					<div className="space-y-4">
						<p className="text-sm text-gray-600">Add a new lead to your CRM.</p>

						<Link
							to="/leads/new"
							className="inline-flex rounded-lg bg-green-600 px-4 py-2 text-white hover:bg-green-700"
						>
							New Lead
						</Link>
					</div>
				</Card>

				<Card title="API Documentation">
					<div className="space-y-4">
						<p className="text-sm text-gray-600">
							Explore the backend API documentation.
						</p>

						<a
							href={`${import.meta.env.VITE_API_URL}/docs/`}
							target="_blank"
							rel="noreferrer"
							className="inline-flex rounded-lg bg-slate-700 px-4 py-2 text-white hover:bg-slate-800"
						>
							Open Swagger
						</a>
					</div>
				</Card>
			</div>
		</div>
	)
}
