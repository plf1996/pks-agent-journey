<template>
  <div class="settings-page">
    <h2 class="settings-page__title">设置</h2>

    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <el-icon><User /></el-icon>
          <span>用户信息</span>
        </div>
      </template>

      <el-descriptions :column="1" border>
        <el-descriptions-item label="用户名">
          {{ authStore.username }}
        </el-descriptions-item>
        <el-descriptions-item label="邮箱">
          {{ authStore.email }}
        </el-descriptions-item>
        <el-descriptions-item label="用户ID">
          {{ authStore.userId }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <el-icon><InfoFilled /></el-icon>
          <span>系统信息</span>
        </div>
      </template>

      <el-descriptions :column="1" border>
        <el-descriptions-item label="系统名称">
          个人知识管理系统 (PKS)
        </el-descriptions-item>
        <el-descriptions-item label="版本">
          v1.0.0
        </el-descriptions-item>
        <el-descriptions-item label="API地址">
          {{ apiBaseUrl }}
        </el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="settings-card">
      <template #header>
        <div class="card-header">
          <el-icon><Operation /></el-icon>
          <span>快捷操作</span>
        </div>
      </template>

      <div class="actions">
        <el-button type="danger" :icon="SwitchButton" @click="handleLogout">
          退出登录
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessageBox } from 'element-plus'
import { User, InfoFilled, Operation, SwitchButton } from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

const apiBaseUrl = computed(() => {
  return import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'
})

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await authStore.logout()
    router.push('/login')
  } catch (error) {
    // 用户取消
  }
}
</script>

<style scoped>
.settings-page {
  padding: 0;
}

.settings-page__title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
}

.settings-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 500;
}

.actions {
  display: flex;
  gap: 12px;
}
</style>
