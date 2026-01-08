import axios from 'axios'
import { ElMessage } from 'element-plus'

// 创建 axios 实例
const request = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 从 localStorage 获取 token
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    const res = response.data

    // 如果 code 为 0，表示成功
    if (res.code === 0) {
      return res.data
    }

    // 其他情况视为错误
    ElMessage.error(res.message || '请求失败')
    return Promise.reject(new Error(res.message || '请求失败'))
  },
  error => {
    console.error('响应错误:', error)

    // 处理 HTTP 状态码
    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          // Token 过期或未认证
          ElMessage.error(data.message || '登录已过期，请重新登录')
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error(data.message || '没有权限访问')
          break
        case 404:
          ElMessage.error(data.message || '请求的资源不存在')
          break
        case 422:
          ElMessage.error(data.message || '数据验证失败')
          break
        case 429:
          ElMessage.error(data.message || '请求过于频繁，请稍后再试')
          break
        case 500:
          ElMessage.error(data.message || '服务器内部错误')
          break
        default:
          ElMessage.error(data.message || `请求失败 (${status})`)
      }
    } else if (error.request) {
      // 请求已发送但没有收到响应
      ElMessage.error('网络错误，请检查您的网络连接')
    } else {
      // 请求配置出错
      ElMessage.error('请求配置错误')
    }

    return Promise.reject(error)
  }
)

export default request
