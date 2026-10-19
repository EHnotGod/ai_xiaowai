<template>
  <header class="main-header">
    <div class="hero-mark" aria-hidden="true">崴<span>AI</span></div>
    <h1>我是 AI 小崴</h1>
    <p>你的校园助手，陪你了解校园、探索知识。</p>
    <div class="topic-tags"><span>校园问答</span><span>知识检索</span><span>图片提问</span></div>
  </header>
</template>

<style scoped>
.main-header { display: flex; flex-direction: column; align-items: center; text-align: center; padding: 32px 0 24px; }
.hero-mark { position: relative; width: 110px; height: 110px; display: grid; place-items: center; background: linear-gradient(135deg, #5d8de9, #70bfc7); border-radius: 32px; color: white; font-size: 58px; box-shadow: 0 16px 36px #3a71e82a; }
.hero-mark span { position: absolute; right: -12px; bottom: -5px; background: #fff; color: #3a71e8; border-radius: 20px; padding: 5px 10px; font: 700 17px system-ui; }
h1 { margin: 28px 0 5px; font-size: 27px; color: #254b70; }
p { color: #586d81; font-size: 15px; line-height: 1.7; }
.topic-tags { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; font-size: 12px; color: #3d638b; }
.topic-tags span { padding: 6px 12px; background: #ffffff9c; border-radius: 20px; }
</style>
