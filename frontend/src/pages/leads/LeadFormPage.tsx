import { useState } from "react"
import { useNavigate } from "react-router-dom"

import { useMutation } from "@tanstack/react-query"
import toast from "react-hot-toast"

import { createLead } from "../../api/leads"

import Card from "../../components/ui/Card"
import PageHeader from "../../components/ui/PageHeader"
import TextField from "../../components/ui/TextField"

export default function LeadFormPage() {
	const navigate = useNavigate()

	const [firstName, setFirstName] = useState("")
	const [lastName, setLastName] = useState("")
	const [email, setEmail] = useState("")
	const [phone, setPhone] = useState("")
	const [company, setCompany] = useState("")
	const [source, setSource] = useState("")

	const mutation = useMutation({
		mutationFn: createLead,

		onSuccess: (lead) => {
			toast.success("Lead created successfully.")

			navigate(`/leads/${lead.id}`)
		},

		onError: () => {
			toast.error("Unable to create lead.")
		},
	})

	function handleSubmit(e: React.FormEvent) {
		e.preventDefault()

		mutation.mutate({
			first_name: firstName,
			last_name: lastName,
			email,
			phone,
			company,
			source,
		})
	}

	return (
		<div className="space-y-6">
			<PageHeader title="Create Lead" description="Create a new lead." />

			<Card>
				<form onSubmit={handleSubmit} className="space-y-5">
					<div className="grid grid-cols-2 gap-5">
						<TextField
							label="First Name"
							value={firstName}
							onChange={(e) => setFirstName(e.target.value)}
							required
						/>

						<TextField
							label="Last Name"
							value={lastName}
							onChange={(e) => setLastName(e.target.value)}
							required
						/>
					</div>

					<TextField
						label="Email"
						type="email"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						required
					/>

					<TextField
						label="Phone"
						value={phone}
						onChange={(e) => setPhone(e.target.value)}
					/>

					<TextField
						label="Company"
						value={company}
						onChange={(e) => setCompany(e.target.value)}
					/>

					<TextField
						label="Source"
						value={source}
						onChange={(e) => setSource(e.target.value)}
					/>

					<div className="flex justify-end">
						<button
							type="submit"
							disabled={mutation.isPending}
							className="rounded-lg bg-blue-600 px-6 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
						>
							{mutation.isPending ? "Creating..." : "Create Lead"}
						</button>
					</div>
				</form>
			</Card>
		</div>
	)
}
