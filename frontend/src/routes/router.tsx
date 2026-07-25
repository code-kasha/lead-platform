import { createBrowserRouter } from "react-router-dom"

import DashboardLayout from "../layouts/DashboardLayout"
import LoginPage from "../pages/auth/LoginPage"
import DashboardPage from "../pages/dashboard/DashboardPage"
import LeadListPage from "../pages/leads/LeadListPage"
import LeadDetailPage from "../pages/leads/LeadDetailPage"
import LeadFormPage from "../pages/leads/LeadFormPage"

export const router = createBrowserRouter([
	{
		path: "/",
		element: <LoginPage />,
	},
	{
		path: "/login",
		element: <LoginPage />,
	},
	{
		element: <DashboardLayout />,
		children: [
			{
				path: "/dashboard",
				element: <DashboardPage />,
			},
		],
	},
	{
		path: "/leads",
		element: <LeadListPage />,
	},
	{
		path: "/leads/:id",
		element: <LeadDetailPage />,
	},
	{
		path: "/leads/new",
		element: <LeadFormPage />,
	},
	{
		path: "/leads/:id/edit",
		element: <LeadFormPage />,
	},
])
