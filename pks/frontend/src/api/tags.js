import request from './index'

/**
 * 创建标签
 * @param {Object} data - 标签数据
 */
export function createTag(data) {
  return request({
    url: '/tags',
    method: 'post',
    data
  })
}

/**
 * 获取标签列表
 * @param {Object} params - 查询参数
 */
export function getTags(params) {
  return request({
    url: '/tags',
    method: 'get',
    params
  })
}

/**
 * 获取标签详情
 * @param {number} tagId - 标签 ID
 */
export function getTagDetail(tagId) {
  return request({
    url: `/tags/${tagId}`,
    method: 'get'
  })
}

/**
 * 更新标签
 * @param {number} tagId - 标签 ID
 * @param {Object} data - 更新数据
 */
export function updateTag(tagId, data) {
  return request({
    url: `/tags/${tagId}`,
    method: 'put',
    data
  })
}

/**
 * 删除标签
 * @param {number} tagId - 标签 ID
 */
export function deleteTag(tagId) {
  return request({
    url: `/tags/${tagId}`,
    method: 'delete'
  })
}
