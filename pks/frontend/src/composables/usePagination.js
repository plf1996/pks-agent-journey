import { ref, computed } from 'vue'
import { PAGINATION_CONFIG } from '@/utils/constants'

/**
 * 分页组合式函数
 * @param {Function} fetchFunction - 获取数据的函数
 * @param {Object} options - 配置选项
 */
export function usePagination(fetchFunction, options = {}) {
  const {
    defaultPageSize = PAGINATION_CONFIG.defaultPageSize,
    pageSizeOptions = PAGINATION_CONFIG.pageSizeOptions
  } = options

  // 分页状态
  const currentPage = ref(1)
  const pageSize = ref(defaultPageSize)
  const total = ref(0)
  const loading = ref(false)

  // 计算总页数
  const totalPages = computed(() => {
    return Math.ceil(total.value / pageSize.value)
  })

  // 获取数据
  const fetchData = async (params = {}) => {
    loading.value = true
    try {
      const data = await fetchFunction({
        page: currentPage.value,
        page_size: pageSize.value,
        ...params
      })

      if (data) {
        total.value = data.total || 0
        currentPage.value = data.page || currentPage.value
      }

      return data
    } catch (error) {
      console.error('获取数据失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 改变页码
  const changePage = (page) => {
    currentPage.value = page
    return fetchData()
  }

  // 改变每页数量
  const changePageSize = (size) => {
    pageSize.value = size
    currentPage.value = 1
    return fetchData()
  }

  // 重置分页
  const resetPagination = () => {
    currentPage.value = 1
    pageSize.value = defaultPageSize
    total.value = 0
  }

  // 分页配置对象
  const paginationConfig = computed(() => ({
    currentPage: currentPage.value,
    pageSize: pageSize.value,
    total: total.value,
    pageSizes: pageSizeOptions,
    layout: 'total, sizes, prev, pager, next, jumper'
  }))

  return {
    // 状态
    currentPage,
    pageSize,
    total,
    loading,
    totalPages,
    paginationConfig,

    // 方法
    fetchData,
    changePage,
    changePageSize,
    resetPagination
  }
}
