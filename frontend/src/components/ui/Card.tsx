// ==============================================================================
// Card Component
// ==============================================================================

import type { ReactNode } from "react"

type CardProps = {
	title?: string
	subtitle?: string
	actions?: ReactNode
	children: ReactNode
	className?: string
}

export default function Card({
	title,
	subtitle,
	actions,
	children,
	className = "",
}: CardProps) {
	return (
		<section
			className={`rounded-xl border border-gray-200 bg-white p-6 shadow-sm transition-shadow hover:shadow-md ${className}`}
		>
			{(title || subtitle || actions) && (
				<header className="mb-6 flex items-start justify-between gap-4 border-b border-gray-100 pb-4">
					<div>
						{title && (
							<h2 className="text-lg font-semibold tracking-tight text-gray-900">
								{title}
							</h2>
						)}

						{subtitle && (
							<p className="mt-1 text-sm text-gray-500">{subtitle}</p>
						)}
					</div>

					{actions && <div className="shrink-0">{actions}</div>}
				</header>
			)}

			<div>{children}</div>
		</section>
	)
}
