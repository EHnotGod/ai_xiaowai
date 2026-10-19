import test from 'node:test'
import assert from 'node:assert/strict'
import { readChatStream } from '../src/api/stream.js'

function stream(bytes, chunkSize) {
  let offset = 0
  return new ReadableStream({
    pull(controller) {
      if (offset >= bytes.length) return controller.close()
      controller.enqueue(bytes.slice(offset, offset + chunkSize))
      offset += chunkSize
    },
  })
}

test('preserves JSON lines and Chinese text at every possible chunk size', async () => {
  const events = [{ response: '你好，校园！' }, { response: '\n第二行' }, { done: true, con_id: 'session-1' }]
  const bytes = new TextEncoder().encode(events.map(JSON.stringify).join('\r\n'))
  for (let chunkSize = 1; chunkSize <= bytes.length; chunkSize++) {
    const received = []
    await readChatStream(stream(bytes, chunkSize), (event) => received.push(event))
    assert.deepEqual(received, events, `chunk size ${chunkSize}`)
  }
})

test('surfaces model errors rather than silently discarding them', async () => {
  const bytes = new TextEncoder().encode('{"response":"部分回复"}\n{"error":"模型服务暂不可用"}\n')
  const received = []
  await assert.rejects(readChatStream(stream(bytes, 7), (event) => received.push(event)), /模型服务暂不可用/)
  assert.deepEqual(received, [{ response: '部分回复' }])
})

test('reports malformed stream data', async () => {
  const bytes = new TextEncoder().encode('not-json\n')
  await assert.rejects(readChatStream(stream(bytes, 3), () => {}), /无法解析/)
})
