import test from 'node:test'
import assert from 'node:assert/strict'
import { apiRequest, readSession, saveSession } from '../src/api/client.js'

function browserSession(t) {
  const saved = new Map()
  const originalStorage = Object.getOwnPropertyDescriptor(globalThis, 'sessionStorage')
  const originalWindow = Object.getOwnPropertyDescriptor(globalThis, 'window')
  Object.defineProperty(globalThis, 'sessionStorage', {
    configurable: true,
    value: { getItem: (key) => saved.get(key) ?? null, setItem: (key, value) => saved.set(key, value), removeItem: (key) => saved.delete(key) },
  })
  Object.defineProperty(globalThis, 'window', { configurable: true, value: new EventTarget() })
  t.after(() => {
    if (originalStorage) Object.defineProperty(globalThis, 'sessionStorage', originalStorage)
    else delete globalThis.sessionStorage
    if (originalWindow) Object.defineProperty(globalThis, 'window', originalWindow)
    else delete globalThis.window
  })
  let expiredEvents = 0
  window.addEventListener('session-expired', () => expiredEvents++)
  return () => expiredEvents
}

const unauthorized = () => new Response(JSON.stringify({ detail: 'Expired' }), { status: 401 })

test('a late 401 from an old account cannot clear the new login', async (t) => {
  const eventCount = browserSession(t)
  let respond
  t.mock.method(globalThis, 'fetch', (_url, options) => {
    assert.equal(options.headers.get('Authorization'), 'Bearer old-token')
    return new Promise((resolve) => { respond = resolve })
  })
  saveSession({ username: 'old-user', access_token: 'old-token' })
  const oldRequest = apiRequest('/history', { json: {} })
  saveSession({ username: 'new-user', access_token: 'new-token' })
  respond(unauthorized())
  await assert.rejects(oldRequest, /登录已失效/)
  assert.deepEqual(readSession(), { username: 'new-user', access_token: 'new-token' })
  assert.equal(eventCount(), 0)
})

test('a current-account 401 clears its token and announces expiry', async (t) => {
  const eventCount = browserSession(t)
  saveSession({ username: 'current-user', access_token: 'current-token' })
  t.mock.method(globalThis, 'fetch', async () => unauthorized())
  await assert.rejects(apiRequest('/history', { json: {} }), /登录已失效/)
  assert.equal(readSession().access_token, '')
  assert.equal(eventCount(), 1)
})

test('a failed login request does not expire another active session', async (t) => {
  const eventCount = browserSession(t)
  saveSession({ username: 'current-user', access_token: 'current-token' })
  t.mock.method(globalThis, 'fetch', async (_url, options) => {
    assert.equal(options.headers.has('Authorization'), false)
    return unauthorized()
  })
  await assert.rejects(apiRequest('/login', { auth: false, json: { username: 'other-user', password: 'wrong-password' } }), /Expired/)
  assert.equal(readSession().access_token, 'current-token')
  assert.equal(eventCount(), 0)
})
