import { createBrowserRouter, Navigate } from "react-router-dom"

import DashboardLayout from "../layouts/DashboardLayout"

import LoginPage from "../pages/auth/LoginPage"
import DashboardPage from "../pages/dashboard/DashboardPage"
import LeadDetailPage from "../pages/leads/LeadDetailPage"
import LeadFormPage from "../pages/leads/LeadFormPage"
import LeadListPage from "../pages/leads/LeadListPage"

export const router = createBrowserRouter([
	{
		path: "/",
		element: <Navigate to="/dashboard" replace />,
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
			{
				path: "/leads",
				element: <LeadListPage />,
			},
			{
				path: "/leads/new",
				element: <LeadFormPage />,
			},
			{
				path: "/leads/:id",
				element: <LeadDetailPage />,
			},
			{
				path: "/leads/:id/edit",
				element: <LeadFormPage />,
			},
		],
	},
])
