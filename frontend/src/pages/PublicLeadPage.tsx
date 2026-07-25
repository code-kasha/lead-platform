// ==============================================================================
// Public Lead Capture Page
// ==============================================================================

import { Link } from "react-router-dom"
import { useState } from "react"

import { useMutation } from "@tanstack/react-query"
import toast from "react-hot-toast"
import { useForm } from "react-hook-form"

import { submitLead, type LeadCreateRequest } from "../api/leads"

import Button from "../components/ui/Button"

import TextField from "../components/ui/TextField"
import Footer from "../components/layout/Footer"

export default function PublicLeadPage() {
	const [submitted, setSubmitted] = useState(false)

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

	const mutation = useMutation({
		mutationFn: submitLead,

		onSuccess: () => {
			reset()
			setSubmitted(true)
			toast.success("Your enquiry has been submitted.")
		},

		onError: () => {
			toast.error("Unable to submit your enquiry.")
		},
	})

	const onSubmit = (data: LeadCreateRequest) => {
		mutation.mutate(data)
	}
	return (
		<div className="flex h-screen flex-col bg-linear-to-br from-slate-50 via-white to-blue-50">
			<header className="border-b bg-white/90 backdrop-blur">
				<div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-6">
					<h1 className="text-xl font-bold text-gray-900">
						Lead Management Platform
					</h1>

					<Link
						to="/login"
						className="rounded-lg bg-blue-600 px-5 py-2 font-medium text-white transition hover:bg-blue-700"
					>
						Login
					</Link>
				</div>
			</header>

			<main className="mx-auto flex w-full max-w-7xl flex-1 items-center px-6 py-16">
				<div className="grid w-full gap-16 lg:grid-cols-2">
					<div className="flex flex-col justify-center">
						<span className="mb-4 inline-flex w-fit rounded-full bg-blue-100 px-4 py-2 text-sm font-semibold text-blue-700">
							Simple CRM for Small Sales Teams
						</span>

						<h2 className="text-5xl font-extrabold leading-tight text-gray-900">
							Capture every sales opportunity.
						</h2>

						<p className="mt-6 max-w-xl text-lg leading-8 text-gray-600">
							Submit your enquiry and our sales team will contact you as soon as
							possible.
						</p>

						<div className="mt-10 grid gap-5 sm:grid-cols-2">
							<div className="rounded-xl border bg-white p-5 shadow-sm">
								<h3 className="font-semibold">Lead Tracking</h3>

								<p className="mt-2 text-sm text-gray-600">
									Every enquiry enters a structured sales pipeline.
								</p>
							</div>

							<div className="rounded-xl border bg-white p-5 shadow-sm">
								<h3 className="font-semibold">Sales Workflow</h3>

								<p className="mt-2 text-sm text-gray-600">
									Assignment, notes, activities and status tracking.
								</p>
							</div>
						</div>
					</div>

					<div className="rounded-2xl border border-gray-200 bg-white p-8 shadow-xl">
						<h3 className="text-2xl font-bold text-gray-900">
							Request a Consultation
						</h3>

						<p className="mt-2 text-gray-600">
							Complete the form below and our sales team will get in touch.
						</p>
						{submitted ? (
							<div className="py-12 text-center">
								<div className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-green-100">
									<span className="text-3xl">✓</span>
								</div>

								<h3 className="mt-6 text-2xl font-bold text-gray-900">
									Thank you!
								</h3>

								<p className="mt-3 text-gray-600">
									Your enquiry has been submitted successfully. Our sales team
									will contact you shortly.
								</p>

								<Button className="mt-8" onClick={() => setSubmitted(false)}>
									Submit Another Lead
								</Button>
							</div>
						) : (
							<form
								onSubmit={handleSubmit(onSubmit)}
								className="mt-8 space-y-5"
							>
								<div className="grid gap-5 md:grid-cols-2">
									<TextField
										label="First Name"
										required
										disabled={mutation.isPending}
										error={errors.first_name?.message}
										{...register("first_name", {
											required: "First name is required",
										})}
									/>

									<TextField
										label="Last Name"
										required
										disabled={mutation.isPending}
										error={errors.last_name?.message}
										{...register("last_name", {
											required: "Last name is required",
										})}
									/>
								</div>

								<TextField
									label="E-mail"
									required
									disabled={mutation.isPending}
									error={errors.email?.message}
									{...register("email", {
										required: "E-mail Address is required",
									})}
								/>

								<div className="grid gap-5 md:grid-cols-2">
									<TextField
										label="Phone"
										required
										disabled={mutation.isPending}
										error={errors.phone?.message}
										{...register("phone", {
											required: "Phone Number is required",
										})}
									/>

									<TextField
										label="Company"
										required
										disabled={mutation.isPending}
										error={errors.company?.message}
										{...register("company", {
											required: "Company is required",
										})}
									/>
								</div>

								<TextField
									label="Source"
									placeholder="Website, Referral, LinkedIn..."
									disabled={mutation.isPending}
									error={errors.source?.message}
									{...register("source", {
										setValueAs: (value: string) => value.trim(),
									})}
								/>

								<Button
									type="submit"
									className="w-full"
									loading={mutation.isPending}
								>
									Submit Lead
								</Button>
							</form>
						)}
					</div>
				</div>
			</main>

			<Footer />
		</div>
	)
}
