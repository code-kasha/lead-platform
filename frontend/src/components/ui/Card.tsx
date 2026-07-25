import type { ReactNode } from "react"

type CardProps = {
	title?: string
	children: ReactNode
	className?: string
}

export default function Card({ title, children, className = "" }: CardProps) {
	return (
		<section
			className={`rounded-lg border bg-white p-6 shadow-sm ${className}`}
		>
			{title && <h2 className="mb-6 text-xl font-semibold">{title}</h2>}

			{children}
		</section>
	)
}
