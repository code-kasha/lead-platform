// ==============================================================================
// Lead Form Page
// ==============================================================================

import { useEffect } from "react"
import { useForm } from "react-hook-form"

import { useNavigate, useParams } from "react-router-dom"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import toast from "react-hot-toast"

import {
	createLead,
	getLead,
	updateLead,
	type Lead,
	type LeadCreateRequest,
} from "../../api/leads"

import Button from "../../components/ui/Button"
import Card from "../../components/ui/Card"
import PageHeader from "../../components/ui/PageHeader"
import Spinner from "../../components/ui/Spinner"
import TextField from "../../components/ui/TextField"

export default function LeadFormPage() {
	const { id } = useParams()

	const navigate = useNavigate()

	const queryClient = useQueryClient()

	const isEdit = Boolean(id)

	// Numeric, matching the key LeadDetailPage reads
	const leadId = Number(id)

	const { data: lead, isLoading } = useQuery({
		queryKey: ["lead", leadId],
		queryFn: () => getLead(leadId),
		enabled: isEdit,
	})

	const {
		register,
		handleSubmit,
		reset,
		formState: { errors },
	} = useForm<LeadCreateRequest>({
		defaultValues: {
			first_name: "",
			last_name: "",
			email: "",
			phone: "",
			company: "",
			source: "",
		},
	})

	useEffect(() => {
		if (!lead) return

		reset({
			first_name: lead.first_name,
			last_name: lead.last_name,
			email: lead.email,
			phone: lead.phone ?? "",
			company: lead.company ?? "",
			source: lead.source ?? "",
		})
	}, [lead, reset])

	const mutation = useMutation<Lead, Error, LeadCreateRequest>({
		mutationFn: (payload) =>
			isEdit ? updateLead(leadId, payload) : createLead(payload),

		onSuccess: (savedLead) => {
			// The detail page shows the saved lead immediately, not stale data
			queryClient.setQueryData(["lead", savedLead.id], savedLead)

			queryClient.invalidateQueries({
				queryKey: ["leads"],
			})

			toast.success(
				isEdit ? "Lead updated successfully." : "Lead created successfully.",
			)

			navigate(`/leads/${savedLead.id}`)
		},

		onError: () => {
			toast.error(isEdit ? "Unable to update lead." : "Unable to create lead.")
		},
	})

	const onSubmit = (data: LeadCreateRequest) => {
		mutation.mutate({
			...data,
			first_name: data.first_name.trim(),
			last_name: data.last_name.trim(),
			email: data.email.trim(),
			phone: data.phone?.trim() ?? "",
			company: data.company?.trim() ?? "",
			source: data.source?.trim() ?? "",
		})
	}

	if (isLoading) {
		return <Spinner label="Loading lead..." />
	}

	return (
		<div className="space-y-6">
			<PageHeader
				title={isEdit ? "Edit Lead" : "Create Lead"}
				description={
					isEdit ? "Update lead information." : "Add a new lead to your CRM."
				}
			/>

			<Card title="Lead Information" subtitle="Complete the details below.">
				<form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
					<div className="grid grid-cols-1 gap-5 md:grid-cols-2">
						<TextField
							label="First Name"
							required
							error={errors.first_name?.message}
							{...register("first_name", {
								required: "First name is required",
							})}
						/>
						<TextField
							label="Last Name"
							required
							error={errors.last_name?.message}
							{...register("last_name", {
								required: "Last name is required",
							})}
						/>
					</div>

					<TextField
						label="Email"
						type="email"
						required
						error={errors.email?.message}
						{...register("email", {
							required: "Email is required",
						})}
					/>

					<div className="grid grid-cols-1 gap-5 md:grid-cols-2">
						<TextField
							label="Phone"
							error={errors.phone?.message}
							{...register("phone")}
						/>

						<TextField
							label="Company"
							error={errors.company?.message}
							{...register("company")}
						/>
					</div>

					<TextField
						label="Source"
						error={errors.source?.message}
						{...register("source")}
					/>

					<div className="flex justify-end gap-3 border-t border-gray-200 pt-6">
						<Button
							type="button"
							variant="secondary"
							onClick={() => navigate(-1)}
						>
							Cancel
						</Button>

						<Button type="submit" loading={mutation.isPending}>
							{isEdit ? "Save Changes" : "Create Lead"}
						</Button>
					</div>
				</form>
			</Card>
		</div>
	)
}
