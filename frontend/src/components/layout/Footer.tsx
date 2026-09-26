// ==============================================================================
// Footer
// ==============================================================================

export default function Footer() {
	return (
		<footer className="border-t border-gray-200 bg-white bottom-0">
			<div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-2 px-6 py-6 text-sm text-gray-500 md:flex-row">
				<p>© {new Date().getFullYear()} Lead Management Platform</p>
			</div>
		</footer>
	)
}
