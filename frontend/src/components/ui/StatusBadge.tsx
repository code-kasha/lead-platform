// ==============================================================================
// Status Badge Component
// ==============================================================================

type StatusBadgeProps = {
	status: string
}

const STATUS_STYLES: Record<
	string,
	{
		label: string
		className: string
	}
> = {
	NEW: {
		label: "New",
		className: "bg-blue-100 text-blue-700",
	},

	CONTACTED: {
		label: "Contacted",
		className: "bg-amber-100 text-amber-700",
	},

	QUALIFIED: {
		label: "Qualified",
		className: "bg-purple-100 text-purple-700",
	},

	PROPOSAL: {
		label: "Proposal",
		className: "bg-indigo-100 text-indigo-700",
	},

	WON: {
		label: "Won",
		className: "bg-emerald-100 text-emerald-700",
	},

	LOST: {
		label: "Lost",
		className: "bg-red-100 text-red-700",
	},
}

export default function StatusBadge({ status }: StatusBadgeProps) {
	const badge = STATUS_STYLES[status] ?? {
		label: status,
		className: "bg-gray-100 text-gray-700",
	}

	return (
		<span
			className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-semibold tracking-wide ${badge.className}`}
		>
			{badge.label}
		</span>
	)
}
