import { Link } from "react-router-dom"

export default function Sidebar() {
	return (
		<aside className="flex h-screen w-64 flex-col border-r bg-white">
			<div className="border-b p-6">
				<h1 className="text-xl font-bold">Lead Manager</h1>
			</div>

			<nav className="flex flex-1 flex-col gap-2 p-4">
				<Link to="/dashboard" className="rounded px-3 py-2 hover:bg-gray-100">
					Dashboard
				</Link>

				<Link to="/leads" className="rounded px-3 py-2 hover:bg-gray-100">
					Leads
				</Link>

				<Link to="/users" className="rounded px-3 py-2 hover:bg-gray-100">
					Users
				</Link>
			</nav>
		</aside>
	)
}
