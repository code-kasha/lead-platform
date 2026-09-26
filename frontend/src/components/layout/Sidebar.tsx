// ==============================================================================
// Sidebar Navigation
// ==============================================================================

import { NavLink, useNavigate } from "react-router-dom"

import { useMutation } from "@tanstack/react-query"
import toast from "react-hot-toast"

import { logout } from "../../api/auth"
import { clearTokens } from "../../utils/token"

export default function Sidebar() {
	const navigate = useNavigate()

	const mutation = useMutation({
		mutationFn: logout,

		onSuccess: () => {
			toast.success("Logged out successfully.")
		},

		// Always drop the local session, even if the server call failed
		onSettled: () => {
			clearTokens()

			navigate("/login", {
				replace: true,
			})
		},
	})

	const linkClass = ({ isActive }: { isActive: boolean }) =>
		`rounded-lg px-4 py-2.5 text-sm font-medium transition ${
			isActive
				? "bg-blue-600 text-white shadow-sm"
				: "text-gray-700 hover:bg-gray-100"
		}`

	return (
		<aside className="flex h-full w-64 shrink-0 flex-col overflow-y-auto border-r border-gray-200 bg-white">
			<div className="border-b border-gray-200 p-6">
				<h1 className="text-xl font-bold tracking-tight text-gray-900">
					Lead Manager
				</h1>

				<p className="mt-1 text-sm text-gray-500">CRM Dashboard</p>
			</div>

			<nav className="flex flex-1 flex-col gap-2 p-4">
				<NavLink to="/dashboard" className={linkClass}>
					Dashboard
				</NavLink>

				<NavLink to="/leads" className={linkClass}>
					Leads
				</NavLink>

				<NavLink to="/profile" className={linkClass}>
					My Profile
				</NavLink>
			</nav>

			<div className="border-t border-gray-200 p-4">
				<button
					type="button"
					onClick={() => mutation.mutate()}
					disabled={mutation.isPending}
					className="w-full rounded-lg bg-red-50 px-4 py-2.5 text-left text-sm font-medium text-red-600 transition hover:bg-red-100 disabled:opacity-50"
				>
					{mutation.isPending ? "Logging out..." : "Logout"}
				</button>
			</div>
		</aside>
	)
}
