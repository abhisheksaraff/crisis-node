import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // Listen on all local IPs
    port: 5173,
    strictPort: true,
    watch: {
      usePolling: true, // Required for HMR to work in Docker/Network volumes
    },
  },
})