import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// If deploying to GitHub Pages as a project site, update base to '/<repo>/'.
export default defineConfig({
  plugins: [vue()],
  base: '/', // change to '/<repo>/' for Pages project site
})
