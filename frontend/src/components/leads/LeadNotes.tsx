import { useState } from "react"

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import toast from "react-hot-toast"

import {
	addLeadNote,
	deleteLeadNote,
	getLeadNotes,
	updateLeadNote,
} from "../../api/leads"

import Card from "../ui/Card"

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

	const addMutation = useMutation({
		mutationFn: () => addLeadNote(leadId, content),

		onSuccess: () => {
			toast.success("Note added.")

			setContent("")

			queryClient.invalidateQueries({
				queryKey: ["lead-notes", leadId],
			})
		},

		onError: () => {
			toast.error("Unable to add note.")
		},
	})

	const updateMutation = useMutation({
		mutationFn: () => updateLeadNote(editingId!, editContent),

		onSuccess: () => {
			toast.success("Note updated.")

			setEditingId(null)
			setEditContent("")

			queryClient.invalidateQueries({
				queryKey: ["lead-notes", leadId],
			})
		},

		onError: () => {
			toast.error("Unable to update note.")
		},
	})

	const deleteMutation = useMutation({
		mutationFn: deleteLeadNote,

		onSuccess: () => {
			toast.success("Note deleted.")

			queryClient.invalidateQueries({
				queryKey: ["lead-notes", leadId],
			})
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
					className="w-full rounded border p-3"
				/>

				<button
					className="mt-3 rounded bg-blue-600 px-4 py-2 text-white"
					onClick={() => addMutation.mutate()}
					disabled={addMutation.isPending || !content.trim()}
				>
					Add Note
				</button>
			</div>

			{isLoading && <p>Loading...</p>}

			{!isLoading && notes?.length === 0 && (
				<p className="text-gray-500">No notes yet.</p>
			)}

			<div className="space-y-4">
				{notes?.map((note) => (
					<div key={note.id} className="rounded border p-4">
						{editingId === note.id ? (
							<textarea
								className="w-full rounded border p-2"
								value={editContent}
								onChange={(e) => setEditContent(e.target.value)}
							/>
						) : (
							<p>{note.content}</p>
						)}

						<div className="mt-4 flex gap-2">
							{editingId === note.id ? (
								<>
									<button
										className="rounded bg-green-600 px-3 py-1 text-white"
										onClick={() => updateMutation.mutate()}
									>
										Save
									</button>

									<button
										className="rounded bg-gray-500 px-3 py-1 text-white"
										onClick={() => setEditingId(null)}
									>
										Cancel
									</button>
								</>
							) : (
								<>
									<button
										className="rounded bg-blue-600 px-3 py-1 text-white"
										onClick={() => {
											setEditingId(note.id)
											setEditContent(note.content)
										}}
									>
										Edit
									</button>

									<button
										className="rounded bg-red-600 px-3 py-1 text-white"
										onClick={() => deleteMutation.mutate(note.id)}
									>
										Delete
									</button>
								</>
							)}
						</div>

						<div className="mt-3 flex justify-between text-sm text-gray-500">
							<span>{note.author.full_name}</span>

							<span>{new Date(note.created_at).toLocaleString()}</span>
						</div>
					</div>
				))}
			</div>
		</Card>
	)
}
