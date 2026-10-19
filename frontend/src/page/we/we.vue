<template>
  <article class="about-page">
    <div class="project-date">校内项目成果 · 2024.11 – 2025.01</div>
    <h1>AI 小崴 · 智能校园助手</h1>
    <p>小崴是面向高校师生的校园服务项目，探索将大模型问答、校园知识检索与常用校园入口整合在同一个界面。</p>
    <h2>项目功能</h2>
    <ul>
      <li>支持流式问答、图片提问和校园资料检索；需自行配置兼容的模型服务和知识库。</li>
      <li>提供用户注册、登录、头像设置以及按账号保存的历史会话。</li>
      <li>保留校园信息入口，地图展示可按自己的校园资料配置。</li>
    </ul>
    <h2>技术实现</h2>
    <p>前端使用 Vue 3、Pinia 和 Element Plus；后端使用 FastAPI、关系数据库，以及可选的 LangChain / FAISS 知识检索。具体部署方式与功能边界见项目 README。</p>
    <h2>当前版本说明</h2>
    <p>这是历史项目整理后的开源版本。原联网搜索、天气服务和第三方全景页面不随代码提供。项目未接入教务账号，不自动查询个人课表，也不代表学校官方服务。</p>
  </article>
</template>

<style scoped>
.about-page { max-width: 820px; padding: 54px 7%; color: #334155; line-height: 1.9; }
.project-date { color: #548093; font-size: 14px; }
h1 { color: #254b70; font-size: 30px; line-height: 1.4; }
h2 { font-size: 20px; margin-top: 32px; }
li { margin: 8px 0; }
</style>
