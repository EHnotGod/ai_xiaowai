import { createApp } from 'vue'
import App from './App.vue'
import {
  ElAvatar, ElButton, ElDialog, ElEmpty, ElForm, ElFormItem, ElInput,
  ElLoading, ElMenu, ElMenuItem, ElTable, ElTableColumn, ElTooltip, ElUpload,
} from 'element-plus'
import 'element-plus/dist/index.css'
import { createPinia } from 'pinia'
// 引入路由实例
import router from "./router/index";
const pinia = createPinia()
const app = createApp(App)
app.use(pinia)
app.use(router);
for (const component of [ElAvatar, ElButton, ElDialog, ElEmpty, ElForm, ElFormItem, ElInput, ElMenu, ElMenuItem, ElTable, ElTableColumn, ElTooltip, ElUpload]) {
  app.component(component.name, component)
}
app.use(ElLoading)
app.mount('#app');
