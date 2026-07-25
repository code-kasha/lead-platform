type InfoRowProps = {
	label: string
	value: React.ReactNode
}

export default function InfoRow({ label, value }: InfoRowProps) {
	return (
		<div>
			<dt className="font-semibold text-gray-600">{label}</dt>

			<dd className="mt-1">{value}</dd>
		</div>
	)
}
