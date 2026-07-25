// ==============================================================================
// Empty State Component
// ==============================================================================

type EmptyStateProps = {
	title: string
	description?: string
}

export default function EmptyState({ title, description }: EmptyStateProps) {
	return (
		<div className="rounded-xl border border-dashed border-gray-300 bg-white px-8 py-16 text-center">
			<h3 className="text-lg font-semibold text-gray-900">{title}</h3>

			{description && (
				<p className="mt-2 text-sm text-gray-500">{description}</p>
			)}
		</div>
	)
}
