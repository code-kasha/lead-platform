// ==============================================================================
// Lead Notes
// ==============================================================================

import { useState } from "react"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import toast from "react-hot-toast"

import {
	addLeadNote,
	deleteLeadNote,
	getLeadNotes,
	updateLeadNote,
} from "../../api/leads"

import Button from "../ui/Button"
import Card from "../ui/Card"
import EmptyState from "../ui/EmptyState"
import Spinner from "../ui/Spinner"

type Props = {
	leadId: number
}

export default function LeadNotes({ leadId }: Props) {
	const queryClient = useQueryClient()

	const [content, setContent] = useState("")
	const [editingId, setEditingId] = useState<number | null>(null)
	const [editContent, setEditContent] = useState("")

	const { data: notes, isLoading } = useQuery({
		queryKey: ["lead-notes", leadId],
		queryFn: () => getLeadNotes(leadId),
	})

	const invalidate = () => {
		queryClient.invalidateQueries({
			queryKey: ["lead-notes", leadId],
		})

		queryClient.invalidateQueries({
			queryKey: ["lead-activities", leadId],
		})
	}

	const addMutation = useMutation({
		mutationFn: () => addLeadNote(leadId, content.trim()),

		onSuccess: () => {
			toast.success("Note added.")

			setContent("")

			invalidate()
		},

		onError: () => {
			toast.error("Unable to add note.")
		},
	})

	const updateMutation = useMutation({
		mutationFn: () => updateLeadNote(editingId!, editContent.trim()),

		onSuccess: () => {
			toast.success("Note updated.")

			setEditingId(null)

			setEditContent("")

			invalidate()
		},

		onError: () => {
			toast.error("Unable to update note.")
		},
	})

	const deleteMutation = useMutation({
		mutationFn: deleteLeadNote,

		onSuccess: () => {
			toast.success("Note deleted.")

			invalidate()
		},

		onError: () => {
			toast.error("Unable to delete note.")
		},
	})

	return (
		<Card title="Notes">
			<div className="mb-6">
				<textarea
					rows={4}
					value={content}
					onChange={(e) => setContent(e.target.value)}
					placeholder="Write a note..."
					className="w-full rounded-lg border border-gray-300 p-3 transition focus:border-blue-500 focus:ring-2 focus:ring-blue-200"
				/>

				<div className="mt-3">
					<Button
						onClick={() => addMutation.mutate()}
						loading={addMutation.isPending}
						disabled={!content.trim()}
					>
						Add Note
					</Button>
				</div>
			</div>

			{isLoading && <Spinner label="Loading notes..." />}

			{!isLoading && notes?.length === 0 && (
				<EmptyState
					title="No Notes"
					description="Add your first note for this lead."
				/>
			)}

			<div className="space-y-4">
				{notes?.map((note) => (
					<div
						key={note.id}
						className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm"
					>
						{editingId === note.id ? (
							<textarea
								value={editContent}
								onChange={(e) => setEditContent(e.target.value)}
								className="w-full rounded-lg border border-gray-300 p-3"
							/>
						) : (
							<p className="leading-7 text-gray-800">{note.content}</p>
						)}

						<div className="mt-4 flex flex-wrap gap-2">
							{editingId === note.id ? (
								<>
									<Button
										variant="success"
										loading={updateMutation.isPending}
										disabled={!editContent.trim()}
										onClick={() => updateMutation.mutate()}
									>
										Save
									</Button>

									<Button
										variant="secondary"
										onClick={() => {
											setEditingId(null)
											setEditContent("")
										}}
									>
										Cancel
									</Button>
								</>
							) : (
								<>
									<Button
										onClick={() => {
											setEditingId(note.id)
											setEditContent(note.content)
										}}
									>
										Edit
									</Button>

									<Button
										variant="danger"
										loading={deleteMutation.isPending}
										onClick={() => deleteMutation.mutate(note.id)}
									>
										Delete
									</Button>
								</>
							)}
						</div>

						<div className="mt-5 flex items-center justify-between border-t pt-3 text-sm text-gray-500">
							<span>{note.author.full_name}</span>

							<span>{new Date(note.created_at).toLocaleString()}</span>
						</div>
					</div>
				))}
			</div>
		</Card>
	)
}
