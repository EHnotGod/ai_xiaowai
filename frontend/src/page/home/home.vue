<template>
    <div class="chat-content">
    <intrograph></intrograph>

    <chatMessage></chatMessage>
    <div style="height:200px" ></div>
    </div>
    <div class="input-content-area">
      <inputArea></inputArea>
    </div>
    
</template>

<script setup>
import { ref, onMounted } from 'vue';
import intrograph from './component/intrograph.vue';
import chatMessage from './component/chatMessage.vue';
import inputArea from "./component/inputArea.vue";

</script>

<style scoped>
.chat-content{
  padding: 100px 200px;
  padding-top: 0;
  margin-top: 50px;
  max-height: 450px;
  overflow-y: auto;
}
  .input-content-area{
    padding:0 200px;
  }
  /* 自定义滚动条的宽度 */
/* 自定义滚动条样式 */
.chat-content {
  overflow-y: auto;  /* 确保内容区域可滚动 */
}

/* 滚动条的宽度 */
.chat-content::-webkit-scrollbar {
  width: 12px;
  opacity: 0;  /* 初始时滚动条透明 */
  transition: opacity 0.3s ease;  /* 平滑过渡效果 */
}

/* 滚动条轨道 */
.chat-content::-webkit-scrollbar-track {
  background: #f0f0f0;
  border-radius: 10px;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.1);
}

/* 滚动条的滑块 */
.chat-content::-webkit-scrollbar-thumb {
  background: linear-gradient(45deg, #8c84c1, #00bcd4);
  border-radius: 10px;
  border: 3px solid #f0f0f0;
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

/* 滑块悬浮效果 */
.chat-content::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(45deg, #8a2be2, #009688);
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.3);
}

/* 鼠标悬停时显示滚动条 */
.chat-content:hover::-webkit-scrollbar {
  opacity: 1;  /* 滚动条显示 */
}


</style>
