import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
const apiUrl = process.env.VITE_API_URL || 'http://backend:8000'


export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/launch': apiUrl
    }
  }
})
