import request from './index'

/**
 * 创建卡片链接（双向）
 * @param {number} cardId - 源卡片 ID
 * @param {Object} data - 链接数据
 * @param {number} data.target_card_id - 目标卡片 ID
 * @param {string} data.link_type - 链接类型 (reference/related/parent)
 */
export function createCardLink(cardId, data) {
  return request({
    url: `/cards/${cardId}/links`,
    method: 'post',
    data
  })
}

/**
 * 获取卡片的所有链接
 * @param {number} cardId - 卡片 ID
 * @param {Object} params - 查询参数
 */
export function getCardLinks(cardId, params) {
  return request({
    url: `/cards/${cardId}/links`,
    method: 'get',
    params
  })
}

/**
 * 删除卡片链接
 * @param {number} cardId - 源卡片 ID
 * @param {number} targetCardId - 目标卡片 ID
 */
export function deleteCardLink(cardId, targetCardId) {
  return request({
    url: `/cards/${cardId}/links/${targetCardId}`,
    method: 'delete'
  })
}
