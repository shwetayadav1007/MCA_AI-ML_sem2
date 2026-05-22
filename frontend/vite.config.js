import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/current-weather': 'http://127.0.0.1:5000',
      '/weather-data': 'http://127.0.0.1:5000',
      '/predict': 'http://127.0.0.1:5000',
      '/train-model': 'http://127.0.0.1:5000',
      '/upload-dataset': 'http://127.0.0.1:5000',
      '/alerts': 'http://127.0.0.1:5000',
      '/health': 'http://127.0.0.1:5000',
    },
  },
})
