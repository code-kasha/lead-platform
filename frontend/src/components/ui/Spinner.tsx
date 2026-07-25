// ==============================================================================
// Spinner Component
// ==============================================================================

type SpinnerProps = {
	label?: string
}

export default function Spinner({ label = "Loading..." }: SpinnerProps) {
	return (
		<div className="flex flex-col items-center justify-center py-16">
			<div className="h-10 w-10 animate-spin rounded-full border-4 border-blue-200 border-t-blue-600" />

			<p className="mt-4 text-sm text-gray-500">{label}</p>
		</div>
	)
}
