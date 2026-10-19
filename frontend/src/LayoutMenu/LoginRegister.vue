<template>
    <el-dialog
      v-model="dialogVisible"
      :title="isLoginMode ? '登录' : '注册'"
      width="30%"
      :modal="true"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      :append-to-body="true"
      class="login-dialog"
    >
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item v-if="!isLoginMode" label="确认密码">
          <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入密码" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog">取消</el-button>
          <el-button type="primary" @click="isLoginMode ? handleLogin() : handleRegister()">
            {{ isLoginMode ? '登录' : '注册' }}
          </el-button>
          <el-button type="text" @click="toggleMode">
            {{ isLoginMode ? '切换到注册' : '切换到登录' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </template>
  
<script setup>
import { API_BASE_URL } from '@/api/config.js';
  import { ref } from 'vue';
  import { ElMessage } from 'element-plus';
  import { userInformation } from '@/api/user.js';
  const UserStore = userInformation();
  const dialogVisible = ref(false);
  const isLoginMode = ref(true); // 默认是登录模式
  const error = ref("");
  // 查询头像的函数
const fetchAvatar = async () => {
  try {
    // 发送 POST 请求
    const response = await fetch(`${API_BASE_URL}/get-avatar`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username: UserStore.username }),
    });

    // 检查请求是否成功
    if (!response.ok) {
      throw new Error('请求失败');
    }

    // 解析响应数据
    const data = await response.json();

    // 处理返回的数据
    if (data.error) {
      error.value = data.error;
    } else {
      UserStore.head = data.base64;
      error.value = ''; // 清空错误信息
    }
  } catch (err) {
    error.value = '请求出错，请稍后重试';
  }
};
  const form = ref({
    username: '',
    password: '',
    confirmPassword: '',
  });
  
  // 打开弹窗
  const openDialog = () => {
    dialogVisible.value = true;
  };
  
  // 关闭弹窗
  const closeDialog = () => {
    dialogVisible.value = false;
  };
  
  // 切换登录/注册模式
  const toggleMode = () => {
    isLoginMode.value = !isLoginMode.value;
    form.value = { username: '', password: '', confirmPassword: '' }; // 清空表单
  };
  
  // 处理登录
  const handleLogin = async () => {
    const { username, password } = form.value;
  
    if (!username || !password) {
      ElMessage.warning('请输入用户名和密码');
      return;
    }
  
    try {
      const response = await fetch(`${API_BASE_URL}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });
  
      if (!response.ok) {
        throw new Error('网络响应异常');
      }
  
      const data = await response.json();
      if (data === true) {
        ElMessage.success('登录成功');
        UserStore.username = username;
        UserStore.is_login = true;
        closeDialog();
        fetchAvatar();
        console.log(UserStore.username);
      } else {
        ElMessage.error('账号或密码错误');
      }
    } catch (error) {
      console.error('登录请求失败:', error);
      ElMessage.error('登录失败，请稍后重试');
    }
  };
  
  // 处理注册
  const handleRegister = async () => {
    const { username, password, confirmPassword } = form.value;
  
    if (!username || !password || !confirmPassword) {
      ElMessage.warning('请填写所有字段');
      return;
    }
  
    if (password !== confirmPassword) {
      ElMessage.warning('两次输入的密码不一致');
      return;
    }
  
    if (!/^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$/.test(password)) {
      ElMessage.warning('密码必须包含字母和数字，且长度至少为6位');
      return;
    }
  
    try {
      // 直接发送注册请求
      const registerResponse = await fetch(`${API_BASE_URL}/zhuce`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: username,
          password: password,
        }),
      });
  
      if (!registerResponse.ok) {
        throw new Error('网络响应异常');
      }
  
      const registerData = await registerResponse.json();
      if (registerData === true) {
        ElMessage.success('注册成功(已登录)');
        UserStore.username = username;
        UserStore.is_login = true;
        closeDialog();
        fetchAvatar();
      } else {
        ElMessage.error('用户名已存在');
      }
    } catch (error) {
      console.error('注册请求失败:', error);
      ElMessage.error('注册失败，请稍后重试');
    }
  };
  
  // 禁用页面滚动
  const disablePageScroll = () => {
    document.body.style.overflow = 'hidden';
  };
  
  // 启用页面滚动
  const enablePageScroll = () => {
    document.body.style.overflow = '';
  };
  
  // 暴露方法，供父组件调用
  defineExpose({
    openDialog,
  });
  </script>
  
  <style scoped>
  .login-dialog {
    z-index: 9999;
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
  </style>