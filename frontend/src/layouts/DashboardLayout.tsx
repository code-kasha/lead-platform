// ==============================================================================
// Dashboard Layout
// ==============================================================================

import { Outlet } from "react-router-dom"

import Sidebar from "../components/layout/Sidebar"
import Topbar from "../components/layout/Topbar"

export default function DashboardLayout() {
	return (
		<div className="flex h-screen flex-col bg-gray-100">
			<Topbar />

			<div className="flex min-h-0 flex-1">
				<Sidebar />

				<main className="min-w-0 flex-1 overflow-y-auto">
					<div className="mx-auto w-full max-w-7xl p-6">
						<Outlet />
					</div>
				</main>
			</div>
		</div>
	)
}
