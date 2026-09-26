import { QueryClient } from "@tanstack/react-query"
import { isAxiosError } from "axios"

// Retry once for network failures and server errors. A 4xx (not found,
// forbidden, invalid page) will get the same answer again, so fail fast.
export function shouldRetry(failureCount: number, error: unknown) {
	if (isAxiosError(error) && error.response && error.response.status < 500) {
		return false
	}

	return failureCount < 1
}

export const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			retry: shouldRetry,
			refetchOnWindowFocus: false,
		},
	},
})
