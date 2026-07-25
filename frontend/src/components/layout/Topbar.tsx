// ==============================================================================
// Top Navigation
// ==============================================================================

import { Link } from "react-router-dom"

export default function Topbar() {
	return (
		<header className="flex h-16 shrink-0 items-center justify-between border-b border-gray-200 bg-white px-6">
			<div>
				<h2 className="text-lg font-semibold text-gray-900">
					Lead Management Platform
				</h2>
			</div>

			<div className="flex items-center gap-4">
				<span className="text-sm text-gray-500">Welcome back</span>

				<Link
					to="/profile"
					className="rounded-lg bg-gray-100 px-3 py-2 text-sm font-medium transition hover:bg-gray-200"
				>
					Profile
				</Link>
			</div>
		</header>
	)
}
