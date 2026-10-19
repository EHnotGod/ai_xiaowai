<template>
  <el-menu :default-active="route.path" router class="campus-menu">
    <el-menu-item index="/"><span class="menu-symbol" aria-hidden="true">◌</span>小崴对话</el-menu-item>
    <el-menu-item index="/map"><span class="menu-symbol" aria-hidden="true">⌖</span>校园地图</el-menu-item>
    <el-menu-item index="/message"><span class="menu-symbol" aria-hidden="true">⌕</span>信息查询</el-menu-item>
    <el-menu-item index="/we"><span class="menu-symbol" aria-hidden="true">ⓘ</span>关于项目</el-menu-item>
  </el-menu>
</template>

<script setup>
import { useRoute } from 'vue-router'
const route = useRoute()
</script>

<style scoped>
.campus-menu { border: 0; background: transparent; }
.menu-symbol { width: 28px; font-size: 24px; }
</style>
