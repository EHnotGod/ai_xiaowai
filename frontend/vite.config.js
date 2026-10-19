import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from "path"
import { fileURLToPath } from 'node:url'
const projectRoot = fileURLToPath(new URL('.', import.meta.url))
// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  resolve:{
    alias:{
      "@":resolve(projectRoot,"./src")
    },
  },
  server: { host: '127.0.0.1', port: 5173, strictPort: true },
});
