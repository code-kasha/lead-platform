type StatusBadgeProps = {
	status: string
}

export default function StatusBadge({ status }: StatusBadgeProps) {
	const classes: Record<string, string> = {
		NEW: "bg-blue-100 text-blue-700",

		CONTACTED: "bg-yellow-100 text-yellow-700",

		QUALIFIED: "bg-green-100 text-green-700",

		LOST: "bg-red-100 text-red-700",

		WON: "bg-emerald-100 text-emerald-700",
	}

	return (
		<span
			className={`rounded px-2 py-1 text-sm font-medium ${
				classes[status] ?? "bg-gray-100 text-gray-700"
			}`}
		>
			{status}
		</span>
	)
}
