import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import { createPinia } from 'pinia'
// 引入路由实例
import router from "./router/index";
const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.use(router);
app.use(ElementPlus);
app.mount('#app');
