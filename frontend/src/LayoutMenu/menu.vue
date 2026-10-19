<template>
    <el-radio-group v-model="isCollapse" style="margin-bottom: 20px">
      <el-radio-button :value="false">Expand</el-radio-button>
      <el-radio-button :value="true">Collapse</el-radio-button>
    </el-radio-group>
    
    <el-menu
      :default-active="activeIndex"
      :collapse="isCollapse"
      @open="handleOpen"
      @close="handleClose"
      class="el-menu-vertical-demo"
      mode="vertical"
      @select="handleSelect"
    >
      <!-- 4个菜单项 -->
      <el-menu-item index="1">
        <el-icon><ChatLineRound /></el-icon>
        <template #title>小崴对话</template>
      </el-menu-item>
  
      <el-menu-item index="2">
        <el-icon><location /></el-icon>
        <template #title>校园地图</template>
      </el-menu-item>
  
      <el-menu-item index="3">
        <el-icon><document /></el-icon>
        <template #title>信息查询</template>
      </el-menu-item>
  
      <el-menu-item index="4">
        <el-icon><setting /></el-icon>
        <template #title>关于我们</template>
      </el-menu-item>
    </el-menu>
  </template>
  
  <script lang="ts" setup>
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'
  import { Location, Menu as IconMenu, Document, Setting, ChatLineRound } from '@element-plus/icons-vue'

  const isCollapse = ref(true)
  const activeIndex = ref('1')  // 默认选中第一个菜单项
  const router = useRouter()
  // 处理菜单展开与收起
  const handleOpen = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
  }
  
  const handleClose = (key: string, keyPath: string[]) => {
    console.log(key, keyPath)
  }
  
  // 判断屏幕宽度是否适合展开菜单
  const updateMenuCollapse = () => {
    if (window.innerWidth < 768) {
      isCollapse.value = true // 小屏幕时折叠菜单
    } else {
      isCollapse.value = false // 大屏幕时展开菜单
    }
  }
  // 菜单项点击时触发的事件
const handleSelect = (index: string) => {
  activeIndex.value = index
  switch (index) {
    case '1':
      router.push('/')         // 跳转到 Home 页
      break
    case '2':
      router.push('/map')   // 跳转到 About 页
      break
    case '3':
      router.push('/message') // 跳转到 Contact 页
      break
    case '4':
      router.push('/we') // 跳转到 Profile 页
      break
  }
}
  
  onMounted(() => {
    updateMenuCollapse()
    window.addEventListener('resize', updateMenuCollapse)
  })
  </script>
  
  <style scoped>
  .el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    /* min-height: 400px; */
  }
  
  @media (max-width: 768px) {
    /* 小屏幕下，默认折叠菜单 */
    .el-menu-vertical-demo {
      width: 60px; /* 收缩后的宽度 */
    }
  }
  </style>
  