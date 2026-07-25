// ==============================================================================
// Button Component
// ==============================================================================

import type { ButtonHTMLAttributes, ReactNode } from "react"

type Variant = "primary" | "secondary" | "danger" | "success"

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
	children: ReactNode
	variant?: Variant
	loading?: boolean
}

const variants: Record<Variant, string> = {
	primary: "bg-blue-600 text-white hover:bg-blue-700 focus:ring-blue-300",

	secondary: "bg-gray-100 text-gray-700 hover:bg-gray-200 focus:ring-gray-300",

	danger: "bg-red-600 text-white hover:bg-red-700 focus:ring-red-300",

	success:
		"bg-emerald-600 text-white hover:bg-emerald-700 focus:ring-emerald-300",
}

export default function Button({
	children,
	variant = "primary",
	loading = false,
	className = "",
	disabled,
	...props
}: ButtonProps) {
	return (
		<button
			{...props}
			disabled={disabled || loading}
			className={`inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition focus:outline-none focus:ring-2 disabled:cursor-not-allowed disabled:opacity-50 ${variants[variant]} ${className}`}
		>
			{loading ? "Please wait..." : children}
		</button>
	)
}
