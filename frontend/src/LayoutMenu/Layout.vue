<template>
  <div class="layout">
    <aside class="sidebar">
      <router-link to="/" class="brand"><span class="brand-mark">崴</span><span>AI 小崴<small>智能校园助手</small></span></router-link>
      <Menu />
      <div class="account-area">
        <el-button v-if="!user.is_login" type="primary" @click="loginDialog.openDialog()">登录 / 注册</el-button>
        <template v-else>
          <Head />
          <Greeting />
          <el-button @click="historyDialog.openDialog()">查看历史会话</el-button>
          <el-button link @click="signOut">退出登录</el-button>
        </template>
      </div>
    </aside>
    <main class="all-content"><router-view /></main>
    <HistoryDialog ref="historyDialog" />
    <LoginRegister ref="loginDialog" />
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import Menu from './menu.vue'
import LoginRegister from './LoginRegister.vue'
import HistoryDialog from './HistoryDialog.vue'
import Head from './head.vue'
import Greeting from './goodeverytime.vue'
import { userInformation } from '@/api/user.js'
import { useChatStore } from '@/api/counter.js'
import { apiRequest } from '@/api/client.js'

const user = userInformation()
const chat = useChatStore()
const loginDialog = ref(null)
const historyDialog = ref(null)
function logout() {
  chat.reset()
  user.logout()
  historyDialog.value?.closeDialog()
}
async function signOut() {
  const token = user.access_token
  logout()
  try {
    await apiRequest('/logout', { auth: false, json: {}, headers: { Authorization: `Bearer ${token}` } })
  } catch { /* Local logout still succeeds if the server cannot be reached. */ }
}
onMounted(() => {
  if (user.is_login) user.fetchAvatar()
  window.addEventListener('session-expired', logout)
})
onUnmounted(() => window.removeEventListener('session-expired', logout))
</script>

<style scoped>
.layout { min-height: 100vh; }
.sidebar { width: 200px; box-sizing: border-box; position: fixed; inset: 0 auto 0 0; background: #ffffffb0; padding: 24px 10px; overflow-y: auto; z-index: 10; }
.brand { display: flex; align-items: center; gap: 10px; margin: 0 8px 28px; color: #254b70; font-size: 21px; font-weight: 700; text-decoration: none; }
.brand small { display: block; font-size: 11px; margin-top: 4px; font-weight: 400; }
.brand-mark { display: grid; place-items: center; background: #3a71e8; color: white; border-radius: 13px; width: 43px; height: 43px; }
.account-area { display: flex; flex-direction: column; align-items: center; gap: 12px; padding-top: 32px; }
.account-area .el-button { margin-left: 0; }
.all-content { margin-left: 200px; min-height: 100vh; }
@media (max-width: 700px) {
  .sidebar { width: 150px; padding: 18px 4px; }
  .brand { gap: 5px; font-size: 17px; margin: 0 6px 18px; }
  .brand-mark { width: 34px; height: 34px; }
  .all-content { margin-left: 150px; }
}
@media (max-width: 480px) {
  .sidebar { width: 120px; }
  .brand-mark { display: none; }
  .all-content { margin-left: 120px; }
  .account-area { padding-top: 20px; }
  .account-area :deep(.el-button) { max-width: 110px; padding: 8px; }
  .account-area :deep(h1) { font-size: 13px; }
}
</style>
