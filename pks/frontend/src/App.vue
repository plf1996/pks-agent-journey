<template>
  <div id="app" class="page-container">
    <router-view v-if="$route.meta.requiresGuest" />
    <template v-else>
      <Header />
      <main class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </main>
      <Footer />
    </template>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import Header from '@/components/common/Header.vue'
import Footer from '@/components/common/Footer.vue'

const router = useRouter()
const authStore = useAuthStore()

onMounted(() => {
  // 检查登录状态
  if (authStore.checkAuth()) {
    // 如果已登录，获取用户信息
    authStore.fetchUserInfo().catch(() => {
      // 获取用户信息失败，可能 token 过期
      authStore.logout()
      router.push('/login')
    })
  }
})
</script>

<style>
#app {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial,
    'Noto Sans', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>
