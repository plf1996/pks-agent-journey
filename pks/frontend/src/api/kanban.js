import request from './index'

/**
 * 获取看板配置
 */
export function getKanban() {
  return request({
    url: '/kanban',
    method: 'get'
  })
}

/**
 * 创建看板列
 * @param {Object} data - 列数据
 */
export function createKanbanColumn(data) {
  return request({
    url: '/kanban/columns',
    method: 'post',
    data
  })
}

/**
 * 更新看板列
 * @param {number} columnId - 列 ID
 * @param {Object} data - 更新数据
 */
export function updateKanbanColumn(columnId, data) {
  return request({
    url: `/kanban/columns/${columnId}`,
    method: 'put',
    data
  })
}

/**
 * 删除看板列
 * @param {number} columnId - 列 ID
 */
export function deleteKanbanColumn(columnId) {
  return request({
    url: `/kanban/columns/${columnId}`,
    method: 'delete'
  })
}

/**
 * 移动卡片到看板列
 * @param {Object} data - 移动数据
 */
export function moveCardToColumn(data) {
  return request({
    url: '/kanban/cards/move',
    method: 'post',
    data
  })
}

/**
 * 批量移动卡片
 * @param {Array<number>} cardIds - 卡片 ID 数组
 * @param {number} targetColumnId - 目标列 ID
 */
export function batchMoveCards(cardIds, targetColumnId) {
  return request({
    url: '/kanban/cards/batch-move',
    method: 'post',
    data: {
      card_ids: cardIds,
      target_column_id: targetColumnId
    }
  })
}
