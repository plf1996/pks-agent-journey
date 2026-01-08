import request from './index'

/**
 * 创建卡片
 * @param {Object} data - 卡片数据
 */
export function createCard(data) {
  return request({
    url: '/cards',
    method: 'post',
    data
  })
}

/**
 * 获取卡片列表
 * @param {Object} params - 查询参数
 */
export function getCards(params) {
  return request({
    url: '/cards',
    method: 'get',
    params
  })
}

/**
 * 获取卡片详情
 * @param {number} cardId - 卡片 ID
 */
export function getCardDetail(cardId) {
  return request({
    url: `/cards/${cardId}`,
    method: 'get'
  })
}

/**
 * 更新卡片
 * @param {number} cardId - 卡片 ID
 * @param {Object} data - 更新数据
 */
export function updateCard(cardId, data) {
  return request({
    url: `/cards/${cardId}`,
    method: 'put',
    data
  })
}

/**
 * 删除卡片
 * @param {number} cardId - 卡片 ID
 */
export function deleteCard(cardId) {
  return request({
    url: `/cards/${cardId}`,
    method: 'delete'
  })
}

/**
 * 批量删除卡片
 * @param {Array<number>} cardIds - 卡片 ID 数组
 */
export function batchDeleteCards(cardIds) {
  return request({
    url: '/cards/batch-delete',
    method: 'post',
    data: { card_ids: cardIds }
  })
}

/**
 * 批量为卡片打标签
 * @param {Array<number>} cardIds - 卡片 ID 数组
 * @param {Array<number>} tagIds - 标签 ID 数组
 */
export function batchTagCards(cardIds, tagIds) {
  return request({
    url: '/cards/batch-tag',
    method: 'post',
    data: {
      card_ids: cardIds,
      tag_ids: tagIds
    }
  })
}
