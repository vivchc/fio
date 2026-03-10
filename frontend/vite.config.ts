import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig(() => ({
	server: {
		port: 5173,
		host: true,
		proxy: {
			'/api': {
				target: 'http://fastapi-dev:8000/',
				rewrite: (path) => path.replace(/^\/api/, '')
			}
		}
	},
	plugins: [react(), tailwindcss()]
}));
