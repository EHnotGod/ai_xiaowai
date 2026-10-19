<template>
  <div class="layout">
    
    <div class="sidebar">
      <img src = "../assets/static/sdu.png" style="width: 100%;"/>
      <Menu></Menu>
      <div class="login-button">
        <el-button type="primary" :icon="Avatar" @click="openLoginDialog">{{ UserStore.is_login ? '切换账户' : '登录/注册' }}</el-button>
      </div>
      <div class="user-head" v-if="UserStore.is_login === true">
        <Head></Head>
        <goodeverytime></goodeverytime>
        <el-button type="primary" @click="handleOpenDialog" class="history">查看历史会话</el-button>
      </div>
    </div>
    <div>
    

    <!-- 使用 HistoryDialog 组件 -->
    <HistoryDialog
      ref="historyDialog"
      :username="username"
      @select-session="handleSelectSession"
    />
  </div>
    <div class="all-content">
      <router-view />
    </div>

    <!-- 使用 LoginRegister 组件 -->
    <LoginRegister ref="loginRegisterRef" />

  </div>
</template>

<script setup>
import { ref } from 'vue';
import { Avatar } from '@element-plus/icons-vue';
import Menu from '@/LayoutMenu/menu.vue';
import LoginRegister from './LoginRegister.vue'; // 引入 LoginRegister 组件
import Head from './head.vue';
import { userInformation } from '@/api/user.js';
import goodeverytime from './goodeverytime.vue';
const UserStore = userInformation();
const loginRegisterRef = ref(null);
import HistoryDialog from './HistoryDialog.vue'; // 引入对话框组件

// 数据
const username = UserStore.username; // 替换为实际的用户名
const historyDialog = ref(null);

// 打开对话框
const handleOpenDialog = () => {
  if (historyDialog.value) {
    historyDialog.value.openDialog(); // 调用子组件的方法
  }
};

// 处理选择的会话
const handleSelectSession = (sessionId) => {
  console.log('在主组件中处理选择的会话ID:', sessionId);
  // 这里可以处理会话选择后的逻辑
};
// 打开登录/注册弹窗
const openLoginDialog = () => {
  loginRegisterRef.value.openDialog();
};
</script>

<style scoped>
.layout {
  display: flex;
}
.sidebar {
  width: 200px;
  position: fixed;
}
.all-content {
  margin-left: 200px;
  width: 100%;
}
.login-button {
  padding: 10px;
}
.user-head {
  width: 100%;
  height: 100px;
  z-index: 9999;
  padding: 10px;
}
.history {
  padding: 10px;
  z-index: 599;
}
</style>