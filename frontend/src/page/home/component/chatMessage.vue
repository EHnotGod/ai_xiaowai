<template>
  <div aria-live="polite" aria-relevant="additions text">
    <article v-for="(message, index) in chat.chatHistory" :key="index" :class="['chat-message', message.type]">
      <div class="message-label">{{ message.type === 'user' ? '你' : '小崴' }}</div>
      <p v-if="message.type === 'user'" class="user-text">{{ message.content }}</p>
      <div v-else-if="message.content" class="markdown-content" v-html="renderMarkdown(message.content)"></div>
      <img v-if="message.picture" :src="message.picture" class="picture" alt="提问附图" />
      <p v-if="message.error" class="error-text" role="alert">{{ message.error }}</p>
    </article>
    <div v-if="chat.loading" class="loading-message"><Loading /><span>小崴正在思考…</span></div>
  </div>
</template>

<script setup>
import Loading from './loading.vue'
import { useChatStore } from '@/api/counter.js'
import { renderMarkdown } from '@/api/markdown.js'
const chat = useChatStore()
</script>

<style scoped>
.chat-message { width: fit-content; max-width: 88%; margin: 20px 0; padding: 14px 18px; border-radius: 16px 16px 16px 4px; background: #fff; overflow-wrap: anywhere; }
.chat-message.user { margin-left: auto; color: #fff; background: #3a71e8; border-radius: 16px 16px 4px 16px; }
.message-label { font-size: 12px; opacity: .7; margin-bottom: 8px; }
.user-text { white-space: pre-wrap; line-height: 1.65; margin: 0; }
.picture { display: block; max-width: 100%; max-height: 240px; border-radius: 8px; margin-top: 10px; }
.error-text { color: #b42318; font-size: 13px; margin-bottom: 0; }
.loading-message { display: flex; align-items: center; gap: 12px; font-size: 13px; color: #4d6580; }
</style>
