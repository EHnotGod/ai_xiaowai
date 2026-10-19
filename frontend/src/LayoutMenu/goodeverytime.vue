<template>
    <div>
      <h1>{{ greeting }}
      {{ UserStore.username }}</h1>
    </div>
  </template>

  <script setup>
  import { computed } from 'vue';
  import { userInformation } from '@/api/user.js';
  const UserStore = userInformation();
  const greeting = computed(() => {
    const hour = new Date().getHours();
    if (hour < 4) {
      return '凌晨好，';
    } else if (hour < 12) {
      return '上午好，';
    } else if (hour < 18) {
      return '下午好，';
    } else {
      return '晚上好，';
    }
  });
  </script>

  <style scoped>
  h1 {
    font-size: 18px;
    color: #333;
  }
  </style>
