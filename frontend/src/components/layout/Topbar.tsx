export default function Topbar() {
	return (
		<header className="flex h-16 items-center justify-between border-b bg-white px-6">
			<h2 className="text-xl font-semibold">Dashboard</h2>

			<button className="rounded bg-red-500 px-4 py-2 text-white">
				Logout
			</button>
		</header>
	)
}
