<template>
    <div class="main-header">
      <!-- 图片容器 -->
      <div class="image-container">
        <ElImage src="https://www.helloimg.com/i/2025/02/05/67a2da7f73682.png" class="header-image"></ElImage>
      </div>
      
      <!-- 文字内容 -->
      <div class="text-container">
        <p class="name-field">我是AI小崴</p>
        <p class="intro-section">你的专属校园助手，可以回答任何问题，帮助你更快地适应校园生活哦！</p>
      </div>
    </div>
  </template>
  
  <script setup>
  </script>
  
  <style scoped lang="less">
  .main-header {
    display: flex;
    flex-direction: column; /* 垂直布局 */
    align-items: center; /* 水平居中 */
    justify-content: flex-start; /* 在顶部对齐 */
    margin-top: 20px; /* 偏上，控制图片上方的间距 */
  }
  
  .image-container {
    display: flex;
    justify-content: center; /* 图片水平居中 */
    margin-bottom: 20px; /* 图片与文字之间的间距 */
    .header-image{
    width: 500px;
    height: auto;
  }
  }
  
  
  
  .text-container {
    text-align: center; /* 文字居中 */
  }
  
  .name-field {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
    font-family: "NAME";
  }
  
  .intro-section {
    font-size: 16px;
    color: #666;
    line-height: 1.5;
  }
  </style>
  