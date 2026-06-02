import { createApp } from 'vue'
import router from './router'
import App from './App.vue'
import './assets/style.css'
// 新增：引入Element Plus组件库及样式
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'

const app = createApp(App)
app.use(router)
app.use(ElementPlus) // 注册Element Plus
app.mount('#app')