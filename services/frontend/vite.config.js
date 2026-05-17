import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    host: '0.0.0.0',
    strictPort: true,
    // Enable HMR to work properly through Nginx gateway proxy
    hmr: {
      path: '/_vite/',
      clientPort: 80
    }
  }
})
