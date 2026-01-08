import { defineStore } from 'pinia'
import { login, register, getCurrentUser, logout as apiLogout } from '@/api/auth'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('access_token') || '',
    refreshToken: localStorage.getItem('refresh_token') || '',
    userInfo: JSON.parse(localStorage.getItem('user_info') || 'null'),
    isLoggedIn: !!localStorage.getItem('access_token')
  }),

  getters: {
    // 获取用户名
    username: (state) => state.userInfo?.username || '',

    // 获取用户 ID
    userId: (state) => state.userInfo?.id || null,

    // 获取邮箱
    email: (state) => state.userInfo?.email || ''
  },

  actions: {
    // 设置 Token
    setToken(access_token, refresh_token) {
      this.token = access_token
      this.refreshToken = refresh_token
      this.isLoggedIn = true
      localStorage.setItem('access_token', access_token)
      localStorage.setItem('refresh_token', refresh_token)
    },

    // 设置用户信息
    setUserInfo(userInfo) {
      this.userInfo = userInfo
      localStorage.setItem('user_info', JSON.stringify(userInfo))
    },

    // 登录
    async login(credentials) {
      try {
        const data = await login(credentials)
        this.setToken(data.access_token, data.refresh_token)
        this.setUserInfo(data.user)
        return data
      } catch (error) {
        throw error
      }
    },

    // 注册
    async register(userData) {
      try {
        const data = await register(userData)
        this.setToken(data.access_token, data.refresh_token)
        this.setUserInfo(data.user)
        return data
      } catch (error) {
        throw error
      }
    },

    // 获取当前用户信息
    async fetchUserInfo() {
      try {
        const userInfo = await getCurrentUser()
        this.setUserInfo(userInfo)
        return userInfo
      } catch (error) {
        throw error
      }
    },

    // 登出
    async logout() {
      try {
        await apiLogout()
      } catch (error) {
        console.error('登出失败:', error)
      } finally {
        this.token = ''
        this.refreshToken = ''
        this.userInfo = null
        this.isLoggedIn = false
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user_info')
      }
    },

    // 检查是否已登录
    checkAuth() {
      const token = localStorage.getItem('access_token')
      const userInfo = localStorage.getItem('user_info')
      if (token && userInfo) {
        this.token = token
        this.refreshToken = localStorage.getItem('refresh_token') || ''
        this.userInfo = JSON.parse(userInfo)
        this.isLoggedIn = true
        return true
      }
      return false
    }
  }
})
