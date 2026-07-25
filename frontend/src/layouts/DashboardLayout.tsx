import { Outlet } from "react-router-dom"

import Sidebar from "../components/layout/Sidebar"
import Topbar from "../components/layout/Topbar"

export default function DashboardLayout() {
	return (
		<div className="flex min-h-screen bg-gray-100">
			<Sidebar />

			<div className="flex min-w-0 flex-1 flex-col">
				<Topbar />

				<main className="flex-1 overflow-y-auto p-6">
					<div className="mx-auto w-full max-w-7xl">
						<Outlet />
					</div>
				</main>
			</div>
		</div>
	)
}
