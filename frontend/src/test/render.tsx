// ==============================================================================
// Test Rendering Helpers
// ==============================================================================

import type { ReactElement } from "react"

import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { render } from "@testing-library/react"
import { createMemoryRouter, RouterProvider } from "react-router-dom"

type RouteOptions = {
	// Route pattern the element is mounted at, e.g. "/leads/:id"
	path: string
	// URL to start at, e.g. "/leads/7"
	url: string
}

// Render an element inside a fresh query client and an in-memory router.
// Returns the router so tests can assert on navigation.
export function renderRoute(element: ReactElement, { path, url }: RouteOptions) {
	const queryClient = new QueryClient({
		defaultOptions: { queries: { retry: false } },
	})

	const router = createMemoryRouter(
		[
			{ path, element },
			{ path: "*", element: <p>Other page</p> },
		],
		{ initialEntries: [url] },
	)

	render(
		<QueryClientProvider client={queryClient}>
			<RouterProvider router={router} />
		</QueryClientProvider>,
	)

	return { router, queryClient }
}
