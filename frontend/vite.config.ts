import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"
import tailwindcss from "@tailwindcss/vite"

export default defineConfig({
	// Read the shared repo-root .env; only VITE_-prefixed keys reach the client
	envDir: "..",
	plugins: [react(), tailwindcss()],
})
