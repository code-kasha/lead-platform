import { useState } from "react"
import { useNavigate } from "react-router-dom"

import { login } from "../../api/auth"
import { setTokens } from "../../utils/token"

export default function LoginPage() {
	const navigate = useNavigate()

	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")

	const [loading, setLoading] = useState(false)

	async function handleSubmit(e: React.FormEvent) {
		e.preventDefault()

		try {
			setLoading(true)

			const response = await login(email, password)

			setTokens(response.data.access, response.data.refresh)

			navigate("/dashboard")
		} finally {
			setLoading(false)
		}
	}

	return (
		<div className="flex min-h-screen items-center justify-center">
			<form
				onSubmit={handleSubmit}
				className="flex w-96 flex-col gap-4 rounded-lg border p-6 shadow"
			>
				<h1 className="text-2xl font-bold">Login</h1>

				<input
					className="rounded border p-2"
					placeholder="Email"
					value={email}
					onChange={(e) => setEmail(e.target.value)}
				/>

				<input
					type="password"
					className="rounded border p-2"
					placeholder="Password"
					value={password}
					onChange={(e) => setPassword(e.target.value)}
				/>

				<button
					disabled={loading}
					className="rounded bg-blue-600 p-2 text-white"
				>
					Login
				</button>
			</form>
		</div>
	)
}
