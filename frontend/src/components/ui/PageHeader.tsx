// ==============================================================================
// Page Header Component
// ==============================================================================

import type { ReactNode } from "react"

type PageHeaderProps = {
	title: string
	description?: string
	action?: ReactNode
}

export default function PageHeader({
	title,
	description,
	action,
}: PageHeaderProps) {
	return (
		<header className="mb-8 flex flex-col gap-4 border-b border-gray-200 pb-6 md:flex-row md:items-start md:justify-between">
			<div className="min-w-0">
				<h1 className="text-3xl font-bold tracking-tight text-gray-900">
					{title}
				</h1>

				{description && (
					<p className="mt-2 max-w-2xl text-sm leading-6 text-gray-500">
						{description}
					</p>
				)}
			</div>

			{action && <div className="shrink-0">{action}</div>}
		</header>
	)
}
