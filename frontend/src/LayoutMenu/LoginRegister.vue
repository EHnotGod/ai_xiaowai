<template>
  <el-dialog v-model="visible" :title="isLogin ? '登录小崴' : '注册账号'" width="min(420px, 92vw)" :close-on-click-modal="false">
    <el-form :model="form" label-position="top" @submit.prevent="submit">
      <el-form-item label="用户名">
        <el-input v-model="form.username" autocomplete="username" :maxlength="32" :disabled="busy" />
      </el-form-item>
      <el-form-item label="密码">
        <el-input v-model="form.password" type="password" show-password :autocomplete="isLogin ? 'current-password' : 'new-password'" :disabled="busy" @keyup.enter="submit" />
      </el-form-item>
      <el-form-item v-if="!isLogin" label="确认密码">
        <el-input v-model="form.confirmPassword" type="password" show-password autocomplete="new-password" :disabled="busy" @keyup.enter="submit" />
      </el-form-item>
      <p v-if="!isLogin" class="form-help">用户名 2 至 32 位，可用中文、字母、数字、下划线、点或短横线；密码 8 至 128 位。</p>
    </el-form>
    <template #footer>
      <el-button :disabled="busy" @click="toggleMode">{{ isLogin ? '创建账号' : '已有账号' }}</el-button>
      <el-button type="primary" :loading="busy" @click="submit">{{ isLogin ? '登录' : '注册并登录' }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { userInformation } from '@/api/user.js'
import { useChatStore } from '@/api/counter.js'

const user = userInformation()
const chat = useChatStore()
const visible = ref(false)
const isLogin = ref(true)
const busy = ref(false)
const form = reactive({ username: '', password: '', confirmPassword: '' })

function clearForm() {
  form.username = ''
  form.password = ''
  form.confirmPassword = ''
}
function toggleMode() {
  isLogin.value = !isLogin.value
  clearForm()
}
function openDialog() {
  clearForm()
  isLogin.value = true
  visible.value = true
}
async function submit() {
  if (busy.value) return
  const username = form.username.trim()
  if (!username || !form.password) return ElMessage.warning('请填写用户名和密码。')
  if (!/^[\p{L}\p{N}_.-]{2,32}$/u.test(username)) return ElMessage.warning('请按要求填写 2 至 32 位的用户名。')
  if (!isLogin.value) {
    if (form.password !== form.confirmPassword) return ElMessage.warning('两次输入的密码不一致。')
    if (form.password.length < 8 || form.password.length > 128) {
      return ElMessage.warning('密码需要 8 至 128 位。')
    }
  }
  busy.value = true
  try {
    await user[isLogin.value ? 'login' : 'register'](username, form.password)
    chat.reset()
    visible.value = false
    clearForm()
    ElMessage.success('登录成功')
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    busy.value = false
  }
}
defineExpose({ openDialog })
</script>

<style scoped>
.form-help { color: #64748b; font-size: 13px; }
</style>
