// Network chunks may split anywhere: in JSON, between lines, or inside UTF-8 text.
export async function readChatStream(body, onEvent) {
  if (!body) throw new Error('服务未返回响应流。')
  const reader = body.getReader()
  const decoder = new TextDecoder()
  let pending = ''
  const parseLine = (line) => {
    if (!line.trim()) return
    let event
    try {
      event = JSON.parse(line)
    } catch {
      throw new Error('服务返回了无法解析的消息，请稍后重试。')
    }
    if (event.error) throw new Error(String(event.error))
    onEvent(event)
  }
  try {
    while (true) {
      const { done, value } = await reader.read()
      pending += done ? decoder.decode() : decoder.decode(value, { stream: true })
      let newline
      while ((newline = pending.indexOf('\n')) >= 0) {
        parseLine(pending.slice(0, newline))
        pending = pending.slice(newline + 1)
      }
      if (done) break
    }
    parseLine(pending)
  } finally {
    await reader.cancel().catch(() => {})
    reader.releaseLock()
  }
}
