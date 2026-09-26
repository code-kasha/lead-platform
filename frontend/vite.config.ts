/// <reference types="vitest/config" />
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
	// Read the shared repo-root .env; only VITE_-prefixed keys reach the client
	envDir: "..",
	plugins: [react(), tailwindcss()],
	test: {
		environment: "jsdom",
		setupFiles: ["./src/test/setup.ts"],
		// Keep tests hermetic: never hit a real backend from a unit test
		env: { VITE_API_URL: "http://api.test/api" },
	},
})
