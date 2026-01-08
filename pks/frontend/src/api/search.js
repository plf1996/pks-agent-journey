import request from './index'

/**
 * 全局搜索
 * @param {Object} params - 搜索参数
 * @param {string} params.q - 搜索关键词
 * @param {string} params.type - 搜索类型 (all/cards/tags)
 * @param {number} params.page - 页码
 * @param {number} params.page_size - 每页数量
 */
export function search(params) {
  return request({
    url: '/search',
    method: 'get',
    params
  })
}

/**
 * 高级搜索
 * @param {Object} data - 搜索数据
 */
export function advancedSearch(data) {
  return request({
    url: '/search/advanced',
    method: 'post',
    data
  })
}
