import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    // Leitet API-Anfragen an das Backend weiter, um CORS-Fehler zu vermeiden
    proxy: {
      '/api': {
        target: 'http://backend:8000', // 'backend' ist der Name des Docker-Services
        changeOrigin: true,
        // Da wir im Docker-Netzwerk sind, brauchen wir keinen rewrite
      }
    }
  }
})
