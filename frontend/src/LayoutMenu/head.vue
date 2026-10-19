<template>
    <div>
      <el-upload
        action="#"
        :auto-upload="false"
        :on-change="handleAvatarChange"
        :show-file-list="false"
      >
      <el-tooltip content="更换头像" placement="right">
        <el-avatar 
          :size="100" 
          :src="UserStore.head"
        />
      </el-tooltip>
      </el-upload>
    </div>
  </template>
  
  <script setup>
import { API_BASE_URL } from '@/api/config.js';
  import { ref } from 'vue';
  import { userInformation } from '@/api/user.js';
  const UserStore = userInformation();
  
  // 处理头像文件变化
  const handleAvatarChange = (file) => {
    const reader = new FileReader();
    reader.onload = (e) => {
      uploadAvatar(e.target.result);
    };
    reader.readAsDataURL(file.raw); // 读取文件为Base64
  };
  
  // 上传头像到后端
  const uploadAvatar = async (base64Image) => {
    try {
      const response = await fetch(`${API_BASE_URL}/upload-avatar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username:UserStore.username,image: base64Image }), // 发送Base64编码的图片
      });
  
      const data = await response.json();
      if (response.ok) {
        console.log('上传成功:', data);
        UserStore.head = base64Image;
      } else {
        console.error('上传失败:', data);
      }
    } catch (error) {
      console.error('上传失败:', error);
    }
  };
  </script>
  

<style>

</style>