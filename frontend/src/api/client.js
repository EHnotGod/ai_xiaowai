export const API_BASE_URL = (import.meta.env?.VITE_API_BASE_URL || 'http://localhost:8000').replace(/\/+$/, '')
const SESSION_KEY = 'ai-xiaowai-session'

export function readSession() {
  try {
    const session = JSON.parse(sessionStorage.getItem(SESSION_KEY) || '{}')
    if (typeof session.username === 'string' && typeof session.access_token === 'string') {
      return { username: session.username, access_token: session.access_token }
    }
  } catch {
    // Invalid or unavailable browser storage starts an anonymous session.
  }
  return { username: '', access_token: '' }
}

export function saveSession(session) {
  sessionStorage.setItem(SESSION_KEY, JSON.stringify({
    username: session.username,
    access_token: session.access_token,
  }))
}

export function clearSession() {
  sessionStorage.removeItem(SESSION_KEY)
}

export async function apiFetch(path, { json, auth = true, ...options } = {}) {
  const headers = new Headers(options.headers)
  const requestToken = auth ? readSession().access_token : ''
  if (auth) {
    if (requestToken) headers.set('Authorization', `Bearer ${requestToken}`)
  }
  if (json !== undefined) headers.set('Content-Type', 'application/json')
  let response
  try {
    response = await fetch(`${API_BASE_URL}${path}`, {
      ...options,
      method: options.method || (json !== undefined ? 'POST' : 'GET'),
      headers,
      ...(json !== undefined ? { body: JSON.stringify(json) } : {}),
    })
  } catch (error) {
    if (error.name === 'AbortError') throw error
    throw new Error('无法连接服务，请检查后端是否启动及 API 地址配置。')
  }
  if (!response.ok) {
    let message = `请求失败（${response.status}）`
    try {
      const data = await response.json()
      if (typeof data.detail === 'string') message = data.detail
      else if (typeof data.error === 'string') message = data.error
      else if (response.status === 422) message = '提交的信息格式不正确，请检查后重试。'
    } catch { /* Keep the HTTP status if the server did not return JSON. */ }
    if (response.status === 401 && auth) {
      if (readSession().access_token === requestToken) {
        clearSession()
        window.dispatchEvent(new Event('session-expired'))
      }
      message = '登录已失效，请重新登录。'
    }
    throw new Error(message)
  }
  return response
}

export async function apiRequest(path, options) {
  return (await apiFetch(path, options)).json()
}
