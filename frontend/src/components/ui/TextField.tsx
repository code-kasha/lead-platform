// ==============================================================================
// Text Field Component
// ==============================================================================

import type { InputHTMLAttributes } from "react"

type TextFieldProps = InputHTMLAttributes<HTMLInputElement> & {
	label: string
	error?: string
	required?: boolean
}

export default function TextField({
	label,
	error,
	required = false,
	className = "",
	id,
	...props
}: TextFieldProps) {
	const inputId = id ?? label.toLowerCase().replace(/\s+/g, "-")

	return (
		<div className="space-y-2">
			<label
				htmlFor={inputId}
				className="block text-sm font-medium text-gray-700"
			>
				{label}

				{required && <span className="ml-1 text-red-500">*</span>}
			</label>

			<input
				id={inputId}
				{...props}
				className={`w-full rounded-lg border border-gray-300 bg-white px-3 py-2 text-sm text-gray-900 transition placeholder:text-gray-400 focus:border-blue-500 focus:ring-2 focus:ring-blue-200 focus:outline-none disabled:cursor-not-allowed disabled:bg-gray-100 disabled:text-gray-500 ${error ? "border-red-500 focus:border-red-500 focus:ring-red-200" : ""} ${className}`}
			/>

			{error && <p className="text-sm text-red-600">{error}</p>}
		</div>
	)
}
