<template>
  <section class="home-page">
    <div ref="messagesArea" class="chat-content">
      <Intrograph v-if="!chat.chatHistory.length" />
      <div v-if="statusMessage" class="service-note" role="status">{{ statusMessage }} <el-button link size="small" :loading="checking" @click="checkService">刷新</el-button></div>
      <ChatMessage />
    </div>
    <footer class="input-content-area"><InputArea /><p class="answer-note">AI 回答可能有误，重要校园信息请以学校官方发布为准。</p></footer>
  </section>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import Intrograph from './component/intrograph.vue'
import ChatMessage from './component/chatMessage.vue'
import InputArea from './component/inputArea.vue'
import { useChatStore } from '@/api/counter.js'
import { apiRequest } from '@/api/client.js'

const chat = useChatStore()
const messagesArea = ref(null)
const health = ref(null)
const connectionError = ref('')
const checking = ref(false)
const statusMessage = computed(() => {
  if (connectionError.value) return connectionError.value
  if (!health.value) return ''
  if (!health.value.llm_configured) return '模型服务尚未配置，请按后端文档设置模型 API。登录、头像和历史记录可独立使用。'
  if (!health.value.rag_ready) return '模型服务已配置；校园知识库尚未就绪，暂不能提供基于校园资料的检索回答。'
  return ''
})
async function checkService() {
  checking.value = true
  try {
    health.value = await apiRequest('/health', { auth: false })
    connectionError.value = ''
  } catch (error) {
    connectionError.value = error.message
  } finally {
    checking.value = false
  }
}
watch(() => [chat.chatHistory.length, chat.chatHistory.at(-1)?.content, chat.loading], async () => {
  await nextTick()
  if (messagesArea.value) messagesArea.value.scrollTop = messagesArea.value.scrollHeight
})
onMounted(checkService)
</script>

<style scoped>
.home-page { height: 100vh; display: flex; flex-direction: column; max-width: 1160px; margin: 0 auto; box-sizing: border-box; }
.chat-content { flex: 1; min-height: 0; overflow-y: auto; padding: 20px 7%; scrollbar-width: thin; }
.input-content-area { padding: 16px 7% 10px; }
.answer-note { text-align: center; color: #637487; font-size: 11px; line-height: 1.5; margin: 9px 0 0; }
.service-note { background: #fff8e8; color: #79551d; border-radius: 10px; padding: 10px 14px; font-size: 13px; line-height: 1.7; }
@media (max-width: 700px) { .chat-content { padding: 12px; } .input-content-area { padding: 10px; } }
</style>
