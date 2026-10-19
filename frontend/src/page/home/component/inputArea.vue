<template>
  <div class="input-box-area">
    <el-input v-model="text" type="textarea" :autosize="{ minRows: 2, maxRows: 6 }" :maxlength="8000" show-word-limit resize="none" :disabled="chat.busy" placeholder="请输入你想了解的校园问题（Ctrl + Enter 发送）" @keydown.ctrl.enter.prevent="send" />
    <div v-if="picture" class="attachment">已选图片：{{ picture.name }}<el-button link :disabled="chat.busy" @click="picture = null">移除</el-button></div>
    <div class="functions">
      <el-button :disabled="chat.busy" @click="newConversation">＋ 新建对话</el-button>
      <el-tooltip content="原联网查询与天气服务未随项目提供，当前未启用。"><span class="feature-note">联网查询未配置</span></el-tooltip>
      <div class="send-actions">
        <input ref="fileInput" type="file" accept="image/png,image/jpeg,image/webp" class="file-input" @change="selectPicture" />
        <el-button :disabled="chat.busy || !user.is_login" aria-label="添加图片" @click="fileInput.click()">▧ 图片</el-button>
        <el-button type="primary" :loading="chat.busy" :disabled="!text.trim() || !user.is_login" @click="send">发送 ↑</el-button>
      </div>
    </div>
    <small v-if="!user.is_login" class="login-hint">请先从左侧登录或注册；对话记录仅对当前账号可见。</small>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useChatStore } from '@/api/counter.js'
import { userInformation } from '@/api/user.js'

const chat = useChatStore()
const user = userInformation()
const text = ref('')
const picture = ref(null)
const fileInput = ref(null)
watch(() => user.access_token, () => {
  text.value = ''
  picture.value = null
})

function newConversation() {
  chat.reset()
  text.value = ''
  picture.value = null
}
function selectPicture(event) {
  const file = event.target.files[0]
  event.target.value = ''
  if (!file) return
  if (!['image/png', 'image/jpeg', 'image/webp'].includes(file.type) || file.size > 5 * 1024 * 1024) {
    return ElMessage.warning('请选择 5 MB 以内的 PNG、JPEG 或 WebP 图片。')
  }
  picture.value = file
}
async function send() {
  if (!text.value.trim() || chat.busy) return
  if (!user.is_login) return ElMessage.warning('请先登录后再开始对话。')
  const prompt = text.value.trim()
  const attachment = picture.value
  const requestToken = user.access_token
  text.value = ''
  picture.value = null
  try {
    await chat.chat(prompt, attachment)
  } catch (error) {
    if (user.access_token === requestToken) {
      text.value = prompt
      picture.value = attachment
      ElMessage.error(error.message)
    }
  }
}
</script>

<style scoped>
.input-box-area { border-radius: 20px; background: #fff; padding: 12px; box-shadow: 0 6px 30px #254b7015; }
.functions { display: flex; justify-content: space-between; align-items: center; gap: 12px; margin-top: 10px; flex-wrap: wrap; }
.send-actions { display: flex; margin-left: auto; }
.file-input { display: none; }
.feature-note, .login-hint { color: #64748b; font-size: 12px; }
.login-hint { display: block; margin-top: 10px; }
.attachment { font-size: 13px; color: #3a71e8; padding-top: 8px; overflow-wrap: anywhere; }
@media (max-width: 700px) { .feature-note { display: none; } .functions { gap: 8px; } }
</style>
