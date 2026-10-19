<template>
  <section class="quick-access-container">
    <h1>信息快速查询</h1>
    <p class="external-note">历史项目收录的校园服务入口，点击后在新窗口打开。部分服务需要校园网络或统一身份认证，地址可能调整。</p>
    <div class="quick-access-grid">
      <a v-for="item in entries" :key="item.label" :href="item.url" target="_blank" rel="noopener noreferrer" class="quick-access-item" :style="{ background: item.color }">
        <span class="entry-symbol" aria-hidden="true">{{ item.label[0] }}</span>
        <h2>{{ item.label }} <span aria-hidden="true">↗</span></h2>
      </a>
    </div>
  </section>
</template>

<script setup>
const entries = [
  { label: '山威主页', color: '#f8d68d', url: 'https://www.wh.sdu.edu.cn/' },
  { label: '信息服务', color: '#82c7d0', url: 'https://service.sdu.edu.cn/tp_up/view?m=up' },
  { label: '自习室查询', color: '#a1d99e', url: 'http://msg.wh.sdu.edu.cn:9008/free-classroom-select.html' },
  { label: '图书馆预约', color: '#fbb7b1', url: 'https://libseat.sdu.edu.cn/home/web/seat/area/156' },
  { label: '学院官网', color: '#e0e0e0', url: 'https://math.wh.sdu.edu.cn/' },
  { label: '培养方案', color: '#8ac5c5', url: 'https://math.wh.sdu.edu.cn/info/1360/26723.htm' },
  { label: '空调电费', color: '#f7a0b6', url: 'https://gyktgd.wh.sdu.edu.cn/dianbiao/AuthServlet.se' },
  { label: '新闻资讯', color: '#a1e2e2', url: 'https://math.wh.sdu.edu.cn/xyxw.htm' },
  { label: '通知公告', color: '#d7f1a1', url: 'https://math.wh.sdu.edu.cn/tzgg.htm' },
  { label: '失物招领', color: '#9fa2d8', url: 'https://msg.wh.sdu.edu.cn/index.html' },
]
</script>

<style scoped>
.quick-access-container { padding: 32px 5%; max-width: 1200px; margin: 0 auto; }
h1 { color: #254b70; font-size: 28px; border-bottom: 2px solid #c4a267; padding-bottom: 14px; }
.external-note { font-size: 13px; color: #64748b; margin-bottom: 28px; line-height: 1.7; }
.quick-access-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 20px; }
.quick-access-item { display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 20px 10px; border-radius: 12px; color: #334155; text-align: center; text-decoration: none; min-height: 120px; box-shadow: 0 4px 6px #00000014; transition: transform .2s; }
.quick-access-item:hover { transform: translateY(-4px); }
.entry-symbol { display: grid; place-items: center; height: 48px; width: 48px; border-radius: 16px; background: #ffffff70; font-size: 26px; }
h2 { margin: 16px 0 0; font-size: 16px; }
@media (max-width: 1100px) { .quick-access-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); } }
@media (max-width: 800px) { .quick-access-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 12px; } }
@media (max-width: 480px) { .quick-access-grid { grid-template-columns: 1fr; } }
</style>
