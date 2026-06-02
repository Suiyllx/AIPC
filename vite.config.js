import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': resolve(__dirname, 'src') // 配置@指向src目录
    }
  },
  server: {
    port: 3000, // 本地运行端口
    open: true, // 启动后自动打开浏览器
    proxy: {
      // 开发时将 /api/* 转发到 Flask 后端（5001 端口，5000 被 macOS AirPlay 占用）
      '/api': {
        target: 'http://localhost:5001',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: 'dist', // 打包输出目录
    assetsDir: 'assets' // 静态资源目录
  }
})