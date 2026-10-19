import { API_BASE_URL } from '@/api/config.js';
import { defineStore } from 'pinia'
import { v4 as uuidv4 } from 'uuid';
import { userInformation } from '@/api/user.js';
const UserStore = userInformation();
export const useChatStore = defineStore('chat', {
  state: () => ({
    userMessage: '',    // 用户输入的消息
    aiResponse: '',     // AI 回复的内容
    converId: '',       // 会话 ID
    loading: false,     // 加载状态
    firstRequest: false,// 是否是第一次请求
	  chatHistory:[],     //历史记录
    picHistory:[],
    is_imggg:false,
    is_web:false
  }),

  actions: {
    async chat() {
        if (this.converId===""){
            const newUuid = uuidv4();
            this.converId = newUuid;
            console.log("已生成对话编号：",newUuid);  // 打印生成的 UUID
        }
        this.loading = true;
        const bodyData = {
            text: this.userMessage,
            con_id: this.converId,
            imggg:this.is_imggg,
            username:UserStore.username,
            history:this.chatHistory,
            pichistory:this.picHistory,
            iswifi:this.is_web
        };
        try {
        const response = await fetch(`${API_BASE_URL}/sdk_run`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(bodyData)
        });
            // 确保响应正常
        if (!response.ok) {
            throw new Error('网络响应失败');
        }
        // 获取响应的可读流
        const reader = response.body.getReader();
        const decoder = new TextDecoder();  // 用于解码流中的文本
        let done = false;
        let content = '';
        while (!done) {
            const { value, done: doneReading } = await reader.read();
            done = doneReading;
            this.loading = false;
            // 解码当前块并处理 JSON
            const chunks = decoder.decode(value, { stream: true });
            const lines = chunks.split("\n");
            for (let i = 0; i < lines.length - 1; i++){
              const chunk = lines[i];
              try {
                // 尝试解析 JSON 数据
                const jsonData = JSON.parse(chunk);
                if (jsonData && jsonData.response) {
                  // 拼接 content
                  content += jsonData.response;
                  this.aiResponse = content; // 更新 UI
                  this.chatHistory[this.chatHistory.length - 1].content = this.aiResponse;
                }
              } catch (e) {
              }
            }
            
          }
        
        console.log("AI 回复:", this.aiResponse);  // 打印 AI 回复
        console.log("历史记录:", this.chatHistory)
      } catch (err) {
        console.error('请求失败', err);
        this.aiResponse = '请求失败'; // 失败时设置 AI 回复为 '请求失败'
      } finally {
        this.loading = false; // 完成加载
        this.userMessage = ""
      }
    },
  }
})
