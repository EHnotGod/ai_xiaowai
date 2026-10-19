<template>
  <section class="map-page">
    <h1>校园地图</h1>
    <p>原项目提供地图图片上的点位展示。地图图片、校园照片和第三方全景素材未包含在开源版本中。</p>
    <iframe v-if="mapUrl" :src="mapUrl" title="已配置的校园地图" referrerpolicy="no-referrer" sandbox="allow-scripts allow-same-origin allow-popups" allowfullscreen></iframe>
    <el-empty v-else description="校园地图尚未配置">
      <p class="map-help">部署者可在环境配置中接入有权使用的校园地图页面。</p>
    </el-empty>
  </section>
</template>

<script setup>
const configuredUrl = import.meta.env.VITE_CAMPUS_MAP_URL || ''
let mapUrl = ''
try {
  const url = new URL(configuredUrl)
  if (['https:', 'http:'].includes(url.protocol)) mapUrl = url.href
} catch { /* An absent or invalid URL keeps the unconfigured state visible. */ }
</script>

<style scoped>
.map-page { padding: 32px 5%; color: #334155; line-height: 1.8; }
h1 { color: #254b70; }
iframe { width: 100%; height: 70vh; margin-top: 20px; border: 0; border-radius: 16px; background: #fff; }
.map-help { color: #64748b; text-align: center; font-size: 13px; }
</style>
