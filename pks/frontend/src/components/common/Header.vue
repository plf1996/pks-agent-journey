<template>
  <header class="header">
    <div class="header__container">
      <div class="header__left">
        <h1 class="header__title">
          <router-link to="/">PKS</router-link>
        </h1>
        <span class="header__subtitle">个人知识管理系统</span>
      </div>

      <nav class="header__nav">
        <router-link to="/" class="header__nav-item" active-class="active">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </router-link>
        <router-link to="/cards" class="header__nav-item" active-class="active">
          <el-icon><Document /></el-icon>
          <span>卡片</span>
        </router-link>
        <router-link to="/tags" class="header__nav-item" active-class="active">
          <el-icon><PriceTag /></el-icon>
          <span>标签</span>
        </router-link>
        <router-link to="/kanban" class="header__nav-item" active-class="active">
          <el-icon><Grid /></el-icon>
          <span>看板</span>
        </router-link>
        <router-link to="/search" class="header__nav-item" active-class="active">
          <el-icon><Search /></el-icon>
          <span>搜索</span>
        </router-link>
      </nav>

      <div class="header__right">
        <el-button @click="showNewCardDialog" type="primary" :icon="Plus">
          新建卡片
        </el-button>

        <el-dropdown @command="handleCommand" trigger="click">
          <div class="header__user">
            <el-avatar :size="32" :icon="UserFilled" />
            <span class="header__username">{{ authStore.username }}</span>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="settings">
                <el-icon><Setting /></el-icon>
                设置
              </el-dropdown-item>
              <el-dropdown-item command="logout" divided>
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { ElMessageBox } from 'element-plus'
import {
  House,
  Document,
  PriceTag,
  Grid,
  Search,
  Plus,
  UserFilled,
  Setting,
  SwitchButton
} from '@element-plus/icons-vue'

const router = useRouter()
const authStore = useAuthStore()

// 显示新建卡片对话框
const showNewCardDialog = () => {
  router.push('/cards/new')
}

// 处理下拉菜单命令
const handleCommand = async (command) => {
  switch (command) {
    case 'settings':
      router.push('/settings')
      break
    case 'logout':
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
      break
  }
}
</script>

<style scoped>
.header {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header__container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.header__left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header__title {
  font-size: 24px;
  font-weight: bold;
  margin: 0;
}

.header__title a {
  color: #409EFF;
  text-decoration: none;
}

.header__subtitle {
  font-size: 14px;
  color: #909399;
}

.header__nav {
  display: flex;
  gap: 8px;
}

.header__nav-item {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 8px 16px;
  border-radius: 4px;
  color: #606266;
  text-decoration: none;
  transition: all 0.3s;
}

.header__nav-item:hover {
  background-color: #f5f7fa;
  color: #409EFF;
}

.header__nav-item.active {
  background-color: #ecf5ff;
  color: #409EFF;
}

.header__right {
  display: flex;
  align-items: center;
  gap: 16px;
}

.header__user {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.header__user:hover {
  background-color: #f5f7fa;
}

.header__username {
  font-size: 14px;
  color: #303133;
}

@media (max-width: 768px) {
  .header__container {
    padding: 0 10px;
  }

  .header__nav {
    display: none;
  }

  .header__subtitle {
    display: none;
  }
}
</style>
