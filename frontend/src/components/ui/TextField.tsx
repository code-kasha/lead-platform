import type { InputHTMLAttributes } from "react"

type TextFieldProps = InputHTMLAttributes<HTMLInputElement> & {
	label: string
}

export default function TextField({
	label,
	className = "",
	...props
}: TextFieldProps) {
	return (
		<div className="space-y-2">
			<label className="block text-sm font-medium text-gray-700">{label}</label>

			<input
				{...props}
				className={`w-full rounded-lg border border-gray-300 px-3 py-2 outline-none transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200 ${className}`}
			/>
		</div>
	)
}
