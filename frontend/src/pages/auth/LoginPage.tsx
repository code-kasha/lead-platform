import { useState } from "react"
import { useLocation, useNavigate } from "react-router-dom"

import { isAxiosError } from "axios"

import { login } from "../../api/auth"
import { setTokens } from "../../utils/token"

function loginErrorMessage(error: unknown) {
	if (isAxiosError(error) && error.response) {
		const detail = error.response.data?.detail

		if (typeof detail === "string") {
			return detail
		}

		if (error.response.status === 400) {
			return "Enter a valid email address and password."
		}
	}

	return "Unable to sign in right now. Please try again."
}

export default function LoginPage() {
	const navigate = useNavigate()
	const location = useLocation()

	// Set by RequireAuth when it redirected here
	const from = (location.state as { from?: string } | null)?.from ?? "/dashboard"

	const [email, setEmail] = useState("")
	const [password, setPassword] = useState("")

	const [loading, setLoading] = useState(false)
	const [error, setError] = useState<string | null>(null)

	async function handleSubmit(e: React.FormEvent) {
		e.preventDefault()

		try {
			setLoading(true)
			setError(null)

			const response = await login(email, password)

			setTokens(response.data.access, response.data.refresh)

			navigate(from, { replace: true })
		} catch (err) {
			setError(loginErrorMessage(err))
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

				{error && (
					<p
						role="alert"
						className="rounded border border-red-200 bg-red-50 p-2 text-sm text-red-700"
					>
						{error}
					</p>
				)}

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
