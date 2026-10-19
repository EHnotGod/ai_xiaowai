<template>
    <div class="input-box-area">
      <div class="input-box">
        <el-input
          v-model="textarea"
          maxlength="300"
          :autosize="{ minRows: 2, maxRows: 6 }"
          placeholder="请输入任何你想问的问题！"
          show-word-limit
          width:auto
          resize="none"
          type="textarea"
        />
      </div>
      <div class="functions-imgs">
        <el-tooltip content="新建对话" placement="right">
        <img src="../../../assets/static/new.png" alt="清除" @click="clearText" class="qingchu-img"></img>
      </el-tooltip>
        <el-switch v-model="chatStore.is_web" active-text="联网查询" inactive-text="关闭" class="web-search" />
        <div class="youce-img">
          <el-upload
            accept='image/jpeg,image/gif,image/png,image/jpg'
            class="upload-img-button"
            :action="`${API_BASE_URL}/upload`"
            method="post"
            list-type="picture"
            limit=1
            v-model:file-list="fileList"
            :data="{ con_id: chatStore.converId }"
            :on-success="UploadSuccess"
          >
          <el-tooltip content="上传图片" placement="left">
            <img 
              src="../../../assets/static/pic.png" 
              alt="上传图片"
              class="send-button-upload-img" 
            />
          </el-tooltip>
          </el-upload>
          <el-tooltip content="发送" placement="right">
          <img 
            src="../../../assets/static/fasong.png"
            alt="发送" 
            @click="sendText" 
            class="send-button" 
            :class="{'sending': isSending, 'sending-back': isSendingBack}"
          />
        </el-tooltip>
        </div>
      </div>
    </div>
  </template>
  
<script setup>
import { API_BASE_URL } from '@/api/config.js';
import { ref } from 'vue'
import { useChatStore } from '@/api/counter.js';
const switchValue = ref('')
const chatStore = useChatStore();
const textarea = ref('')
const isSending = ref(false)  // 控制按钮飞出的动画状态
const isSendingBack = ref(false)  // 控制按钮飞回的动画状态
const fileList = ref([]);
// 清除输入框内容
const clearText = () => {
  chatStore.converId = "";
  chatStore.chatHistory = [];
  chatStore.picHistory = [];
  chatStore.loading = false;
  chatStore.aiResponse = "";
  chatStore.userMessage = "";
  textarea.value = ''
}

const UploadSuccess = (response) => {
  console.log(response);
  if (chatStore.converId === "" && response){
    chatStore.converId = response;
  }
}
  
// 发送输入框内容
const sendText = () => {
  if (textarea.value.trim()) {
    const reader = new FileReader();

    console.log("发送内容:", textarea.value)
    isSending.value = true
    chatStore.userMessage = textarea.value
    chatStore.chatHistory.push({ type: 'user', content: chatStore.userMessage });
    chatStore.chatHistory.push({ type: 'ai', content: "" });
    if (fileList.value.length === 0) {
      chatStore.is_imggg = false;
      chatStore.picHistory.push("");
    } else {
      chatStore.is_imggg = true;
      
      // 这里需要使用 FileReader 异步读取文件
      const reader = new FileReader();
      reader.onloadend = () => {
        chatStore.picHistory.push(reader.result);  // 获取到 Base64 数据
        console.log(chatStore.picHistory);
      };
      reader.onerror = (error) => {
        console.error("文件读取失败", error);
      };
      reader.readAsDataURL(fileList.value[0].raw);  // 读取图片
    }
    chatStore.chat();
    textarea.value = ''  // 清空输入框
    fileList.value = [];
    console.log(fileList);

    // 触发飞回动画
    setTimeout(() => {
      isSending.value = false
      isSendingBack.value = true

      // 清空输入框并等待动画结束后恢复状态
      setTimeout(() => {
        isSendingBack.value = false
        
      }, 200)  // 动画时长，确保飞回动画完整执行
    }, 200)  // 飞出动画时长
  }
}
</script>
  
  <style lang="less" scoped>
  .input-box-area {
    border-radius: 20px;
    background-color: #ffffff;
    display: flex;
    flex-direction: column;
    padding: 5px;
    
    .input-box {
      padding: 5px;
      justify-content: center;
    }
  
    .functions-imgs {
      display: flex;
      justify-content: space-between;  /* 使按钮分别对齐左右两端 */
      padding-inline: 10px;
      padding-top: 5px;
      .youce-img{
        display: flex;
        flex-direction:row;
        gap:20px;
      }
      .qingchu-img, .send-button,.send-button-upload-img{
        width: 27px;
        height: 27px;
        cursor: pointer;
      }
    }
}
  /* 使用 fixed 来固定输入框位置 */
.input-box-area {
  position: fixed;  /* 固定定位 */
  width:calc(100% - 625px);
  bottom: 50px;  /* 距离页面底部 20px */
  z-index: 500;   /* 确保输入框位于页面的最上层 */
}
  /* 飞出并渐隐动画 */
  .send-button {
    transition: transform 0.3s ease, opacity 0.3s ease;
  }
  
  .send-button.sending {
    transform: translate(50px, -50px);  /* 向右上角飞出 */
    opacity: 0;  /* 渐隐 */
  }
  
  /* 飞回并彻底渐隐 */
  .send-button.sending-back {
    transform: translate(-50px, 50px);  /* 从左下角飞回 */
    opacity: 0;  /* 保持不可见 */
  }
  </style>
  