import { defineConfig } from 'vite'

export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://web:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
}) 