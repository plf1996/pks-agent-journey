import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresGuest: true, title: '登录' }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresGuest: true, title: '注册' }
  },
  {
    path: '/',
    component: () => import('@/views/Home.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue'),
        meta: { title: '首页' }
      },
      {
        path: 'cards',
        name: 'Cards',
        component: () => import('@/views/Cards.vue'),
        meta: { title: '卡片管理' }
      },
      {
        path: 'cards/:id',
        name: 'CardDetail',
        component: () => import('@/views/CardDetail.vue'),
        meta: { title: '卡片详情' }
      },
      {
        path: 'cards/new',
        name: 'NewCard',
        component: () => import('@/views/CardEditor.vue'),
        meta: { title: '新建卡片' }
      },
      {
        path: 'cards/:id/edit',
        name: 'EditCard',
        component: () => import('@/views/CardEditor.vue'),
        meta: { title: '编辑卡片' }
      },
      {
        path: 'tags',
        name: 'Tags',
        component: () => import('@/views/Tags.vue'),
        meta: { title: '标签管理' }
      },
      {
        path: 'kanban',
        name: 'Kanban',
        component: () => import('@/views/Kanban.vue'),
        meta: { title: '看板视图' }
      },
      {
        path: 'search',
        name: 'Search',
        component: () => import('@/views/Search.vue'),
        meta: { title: '搜索' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/Settings.vue'),
        meta: { title: '设置' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: { title: '页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  // 设置页面标题
  document.title = to.meta.title
    ? `${to.meta.title} - ${import.meta.env.VITE_APP_TITLE || 'PKS'}`
    : import.meta.env.VITE_APP_TITLE || '个人知识管理系统'

  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    if (!authStore.isLoggedIn) {
      // 未登录，跳转到登录页
      next({
        name: 'Login',
        query: { redirect: to.fullPath }
      })
      return
    }
  }

  // 检查是否需要游客状态（已登录用户不能访问登录/注册页）
  if (to.meta.requiresGuest) {
    if (authStore.isLoggedIn) {
      // 已登录，跳转到首页
      next({ name: 'Dashboard' })
      return
    }
  }

  next()
})

export default router
