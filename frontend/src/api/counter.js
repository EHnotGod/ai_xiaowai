import { defineStore } from 'pinia'
import { apiFetch } from './client.js'
import { readChatStream } from './stream.js'
import { userInformation } from './user.js'

let activeRequest = null

function readPicture(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader()
    reader.onload = () => resolve(reader.result)
    reader.onerror = () => reject(new Error('图片读取失败，请重新选择。'))
    reader.readAsDataURL(file)
  })
}

export const useChatStore = defineStore('chat', {
  state: () => ({ converId: '', chatHistory: [], busy: false, loading: false }),
  actions: {
    reset() {
      activeRequest?.abort()
      activeRequest = null
      this.$reset()
    },
    loadConversation(sessionId, messages) {
      this.reset()
      this.converId = sessionId
      this.chatHistory = messages.map((message) => ({ ...message }))
    },
    async chat(text, picture = null) {
      if (this.busy) return
      if (!userInformation().is_login) throw new Error('请先登录后再开始对话。')
      const controller = new AbortController()
      activeRequest = controller
      const isCurrent = () => activeRequest === controller && !controller.signal.aborted
      this.busy = true
      this.loading = true
      let replyIndex = -1
      try {
        let pictureData = ''
        if (picture) {
          pictureData = await readPicture(picture)
          if (!isCurrent()) return
          const upload = new FormData()
          upload.append('file', picture)
          const query = this.converId ? `?con_id=${encodeURIComponent(this.converId)}` : ''
          const uploaded = await apiFetch(`/upload${query}`, {
            method: 'POST', body: upload, signal: controller.signal,
          })
          const conversationId = await uploaded.json()
          if (!isCurrent()) return
          this.converId = conversationId
        }
        if (!isCurrent()) return
        this.chatHistory.push({ type: 'user', content: text, picture: pictureData })
        replyIndex = this.chatHistory.push({ type: 'ai', content: '' }) - 1
        const response = await apiFetch('/sdk_run', {
          json: { text, con_id: this.converId || null, imggg: Boolean(picture), iswifi: false },
          signal: controller.signal,
        })
        if (!isCurrent()) {
          await response.body?.cancel()
          return
        }
        let completed = false
        await readChatStream(response.body, (event) => {
          if (!isCurrent()) return
          if (event.con_id) this.converId = event.con_id
          if (typeof event.response === 'string') {
            this.chatHistory[replyIndex].content += event.response
            this.loading = false
          }
          if (event.done) completed = true
        })
        if (!isCurrent()) return
        if (!completed) throw new Error('连接已中断，回复可能不完整，请稍后重试。')
      } catch (error) {
        if (isCurrent() && error.name !== 'AbortError') {
          if (replyIndex >= 0 && this.chatHistory[replyIndex]) {
            this.chatHistory[replyIndex].error = error.message
          }
          throw error
        }
      } finally {
        if (activeRequest === controller) {
          this.busy = false
          this.loading = false
          activeRequest = null
        }
      }
    },
  },
})
