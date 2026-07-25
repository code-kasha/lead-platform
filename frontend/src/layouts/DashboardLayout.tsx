import { Outlet } from "react-router-dom"

import Sidebar from "../components/layout/Sidebar"
import Topbar from "../components/layout/Topbar"

export default function DashboardLayout() {
	return (
		<div className="flex min-h-screen">
			<Sidebar />

			<div className="flex flex-1 flex-col">
				<Topbar />

				<main className="flex-1 bg-gray-50 p-6">
					<Outlet />
				</main>
			</div>
		</div>
	)
}
