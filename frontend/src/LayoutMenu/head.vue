<template>
  <el-upload action="#" accept="image/png,image/jpeg,image/webp" :auto-upload="false" :on-change="changeAvatar" :show-file-list="false" :disabled="uploading">
    <el-tooltip content="更换头像（PNG / JPEG / WebP，最大 2 MB）" placement="right">
      <el-avatar :size="72" :src="user.head">{{ user.username.slice(0, 1).toUpperCase() }}</el-avatar>
    </el-tooltip>
  </el-upload>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { userInformation } from '@/api/user.js'
import { apiRequest } from '@/api/client.js'
const user = userInformation()
const uploading = ref(false)

async function changeAvatar(file) {
  if (!['image/png', 'image/jpeg', 'image/webp'].includes(file.raw.type) || file.raw.size > 2 * 1024 * 1024) {
    return ElMessage.warning('请选择 2 MB 以内的 PNG、JPEG 或 WebP 图片。')
  }
  uploading.value = true
  const requestToken = user.access_token
  try {
    const image = await new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = () => resolve(reader.result)
      reader.onerror = () => reject(new Error('头像读取失败。'))
      reader.readAsDataURL(file.raw)
    })
    if (user.access_token !== requestToken) return
    await apiRequest('/upload-avatar', { json: { image } })
    if (user.access_token !== requestToken) return
    user.head = image
    ElMessage.success('头像已更新')
  } catch (error) {
    ElMessage.error(error.message)
  } finally {
    uploading.value = false
  }
}
</script>
