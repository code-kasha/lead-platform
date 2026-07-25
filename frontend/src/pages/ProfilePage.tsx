// ==============================================================================
// Profile Page
// ==============================================================================

import { useQuery } from "@tanstack/react-query"

import { me } from "../api/auth"

import Card from "../components/ui/Card"
import InfoRow from "../components/ui/InfoRow"
import PageHeader from "../components/ui/PageHeader"

export default function ProfilePage() {
	const {
		data: user,
		isLoading,
		isError,
	} = useQuery({
		queryKey: ["me"],
		queryFn: me,
	})

	if (isLoading) {
		return (
			<div className="py-20 text-center text-gray-500">Loading profile...</div>
		)
	}

	if (isError || !user) {
		return (
			<div className="py-20 text-center text-red-600">
				Unable to load profile.
			</div>
		)
	}

	return (
		<div className="space-y-6">
			<PageHeader
				title="My Profile"
				description="View your account information."
			/>

			<Card title="Account Information">
				<div className="grid grid-cols-1 gap-6 md:grid-cols-2">
					<InfoRow
						label="Name"
						value={`${user.first_name} ${user.last_name}`}
					/>

					<InfoRow label="Email" value={user.email} />

					<InfoRow label="Role" value={user.role} />

					{"created_at" in user && (
						<InfoRow
							label="Joined"
							value={new Date(user.created_at as string).toLocaleDateString()}
						/>
					)}
				</div>
			</Card>
		</div>
	)
}
