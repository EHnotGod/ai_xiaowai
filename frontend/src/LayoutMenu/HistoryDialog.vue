<template>
  <el-dialog v-model="visible" title="历史会话" width="min(720px, 94vw)">
    <div v-loading="loading">
      <el-table :data="history" empty-text="还没有保存的会话">
        <el-table-column prop="session_id" label="会话" min-width="180">
          <template #default="{ row }">
            <el-button link type="primary" @click="selectSession(row.session_id)">{{ row.session_id.slice(0, 8) }}</el-button>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" min-width="180" />
      </el-table>
    </div>
  </el-dialog>
  <el-dialog v-model="conversationVisible" title="对话记录" width="min(800px, 94vw)">
    <div class="history-messages">
      <article v-for="(message, index) in messages" :key="index" :class="['history-message', message.type]">
        <strong>{{ message.type === 'user' ? '你' : '小崴' }}</strong>
        <p v-if="message.type === 'user'">{{ message.content }}</p>
        <div v-else class="markdown-content" v-html="renderMarkdown(message.content)"></div>
        <img v-if="message.picture" :src="message.picture" alt="此条提问的附件" />
      </article>
    </div>
    <template #footer>
      <el-button @click="conversationVisible = false">关闭</el-button>
      <el-button type="primary" :disabled="chat.busy" @click="continueConversation">继续此会话</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { apiRequest } from '@/api/client.js'
import { useChatStore } from '@/api/counter.js'
import { renderMarkdown } from '@/api/markdown.js'

const router = useRouter()
const chat = useChatStore()
const visible = ref(false)
const conversationVisible = ref(false)
const loading = ref(false)
const history = ref([])
const messages = ref([])
const selectedSession = ref('')
let requestGeneration = 0

async function openDialog() {
  const generation = ++requestGeneration
  visible.value = true
  history.value = []
  loading.value = true
  try {
    const data = await apiRequest('/history', { json: {} })
    if (generation !== requestGeneration) return
    history.value = (data.history || []).sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
  } catch (error) {
    if (generation === requestGeneration) ElMessage.error(error.message)
  } finally {
    if (generation === requestGeneration) loading.value = false
  }
}
async function selectSession(sessionId) {
  const generation = ++requestGeneration
  loading.value = true
  try {
    const data = await apiRequest('/get_conversation', { json: { session_id: sessionId } })
    if (generation !== requestGeneration) return
    messages.value = data.messages || []
    selectedSession.value = sessionId
    visible.value = false
    conversationVisible.value = true
  } catch (error) {
    if (generation === requestGeneration) ElMessage.error(error.message)
  } finally {
    if (generation === requestGeneration) loading.value = false
  }
}
function continueConversation() {
  chat.loadConversation(selectedSession.value, messages.value)
  conversationVisible.value = false
  router.push('/')
}
function closeDialog() {
  requestGeneration++
  visible.value = false
  conversationVisible.value = false
  messages.value = []
  history.value = []
}
defineExpose({ openDialog, closeDialog })
</script>

<style scoped>
.history-messages { max-height: 60vh; overflow-y: auto; }
.history-message { padding: 16px; border-radius: 12px; margin-bottom: 12px; background: #f2f6fc; }
.history-message.user { margin-left: 10%; background: #e7f0ff; }
.history-message.ai { margin-right: 10%; }
.history-message p { white-space: pre-wrap; }
.history-message img { max-height: 160px; max-width: 100%; border-radius: 8px; }
</style>
