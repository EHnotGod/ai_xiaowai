import { defineStore } from 'pinia'
import { apiRequest, clearSession, readSession, saveSession } from './client.js'

export const userInformation = defineStore('user', {
  state: () => ({ ...readSession(), head: '' }),
  getters: {
    is_login: (state) => Boolean(state.access_token),
  },
  actions: {
    async login(username, password) {
      const session = await apiRequest('/login', {
        auth: false,
        json: { username: username.trim(), password },
      })
      saveSession(session)
      this.username = session.username
      this.access_token = session.access_token
      this.head = ''
      await this.fetchAvatar()
    },
    async register(username, password) {
      await apiRequest('/zhuce', {
        auth: false,
        json: { username: username.trim(), password },
      })
      await this.login(username, password)
    },
    async fetchAvatar() {
      const username = this.username
      try {
        const avatar = await apiRequest('/get-avatar', { json: { username } })
        if (this.username === username) this.head = avatar.base64 || ''
      } catch {
        // An unavailable avatar should not turn a successful login into a failure.
        if (this.username === username) this.head = ''
      }
    },
    logout() {
      clearSession()
      this.username = ''
      this.access_token = ''
      this.head = ''
    },
  },
})
