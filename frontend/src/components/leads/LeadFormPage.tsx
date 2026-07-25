import { useEffect, useState } from "react"
import { useNavigate, useParams } from "react-router-dom"

import { useMutation, useQuery } from "@tanstack/react-query"
import toast from "react-hot-toast"

import {
	createLead,
	getLead,
	updateLead,
	type Lead,
	type LeadCreateRequest,
} from "../../api/leads"

import Card from "../../components/ui/Card"
import PageHeader from "../../components/ui/PageHeader"
import TextField from "../../components/ui/TextField"

export default function LeadFormPage() {
	const { id } = useParams()

	const navigate = useNavigate()

	const isEdit = id !== undefined

	const { data: lead, isLoading } = useQuery({
		queryKey: ["lead", id],
		queryFn: () => getLead(Number(id)),
		enabled: isEdit,
	})

	const [firstName, setFirstName] = useState("")
	const [lastName, setLastName] = useState("")
	const [email, setEmail] = useState("")
	const [phone, setPhone] = useState("")
	const [company, setCompany] = useState("")
	const [source, setSource] = useState("")

	useEffect(() => {
		if (!lead) {
			return
		}

		setFirstName(lead.first_name)
		setLastName(lead.last_name)
		setEmail(lead.email)
		setPhone(lead.phone ?? "")
		setCompany(lead.company ?? "")
		setSource(lead.source ?? "")
	}, [lead])

	const mutation = useMutation<Lead, Error, LeadCreateRequest>({
		mutationFn: (data) =>
			isEdit ? updateLead(Number(id), data) : createLead(data),

		onSuccess: (lead) => {
			toast.success(isEdit ? "Lead updated." : "Lead created.")

			navigate(`/leads/${lead.id}`)
		},

		onError: () => {
			toast.error(isEdit ? "Unable to update lead." : "Unable to create lead.")
		},
	})

	function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
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

	if (isLoading) {
		return <div className="py-20 text-center">Loading lead...</div>
	}

	return (
		<div className="space-y-6">
			<PageHeader
				title={isEdit ? "Edit Lead" : "Create Lead"}
				description={isEdit ? "Update lead information." : "Create a new lead."}
			/>

			<Card>
				<form onSubmit={handleSubmit} className="space-y-5">
					<div className="grid grid-cols-1 gap-5 md:grid-cols-2">
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
							className="rounded-lg bg-blue-600 px-6 py-2 text-white transition hover:bg-blue-700 disabled:opacity-50"
						>
							{mutation.isPending
								? isEdit
									? "Saving..."
									: "Creating..."
								: isEdit
									? "Save Changes"
									: "Create Lead"}
						</button>
					</div>
				</form>
			</Card>
		</div>
	)
}
