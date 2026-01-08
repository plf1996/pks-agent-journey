/**
 * 卡片类型常量
 */
export const CARD_TYPES = {
  NOTE: 'note',
  LINK: 'link',
  IMAGE: 'image',
  CODE: 'code'
}

/**
 * 卡片类型选项
 */
export const CARD_TYPE_OPTIONS = [
  { label: '笔记', value: CARD_TYPES.NOTE, icon: 'Document' },
  { label: '链接', value: CARD_TYPES.LINK, icon: 'Link' },
  { label: '图片', value: CARD_TYPES.IMAGE, icon: 'Picture' },
  { label: '代码', value: CARD_TYPES.CODE, icon: 'Code' }
]

/**
 * 链接类型常量
 */
export const LINK_TYPES = {
  REFERENCE: 'reference',
  RELATED: 'related',
  PARENT: 'parent'
}

/**
 * 链接类型选项
 */
export const LINK_TYPE_OPTIONS = [
  { label: '引用', value: LINK_TYPES.REFERENCE, color: '#409EFF' },
  { label: '相关', value: LINK_TYPES.RELATED, color: '#67C23A' },
  { label: '父级', value: LINK_TYPES.PARENT, color: '#E6A23C' }
]

/**
 * 排序字段选项
 */
export const SORT_OPTIONS = [
  { label: '创建时间', value: 'created_at' },
  { label: '更新时间', value: 'updated_at' },
  { label: '浏览次数', value: 'view_count' }
]

/**
 * 排序方向选项
 */
export const ORDER_OPTIONS = [
  { label: '降序', value: 'desc' },
  { label: '升序', value: 'asc' }
]

/**
 * 分页默认配置
 */
export const PAGINATION_CONFIG = {
  defaultPageSize: 20,
  pageSizeOptions: [10, 20, 50, 100],
  showSizeChanger: true,
  showTotal: (total) => `共 ${total} 条`
}

/**
 * 本地存储键名
 */
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_INFO: 'user_info',
  THEME: 'theme',
  LANGUAGE: 'language'
}

/**
 * 默认标签颜色
 */
export const DEFAULT_TAG_COLORS = [
  '#409EFF', '#67C23A', '#E6A23C', '#F56C6C', '#909399',
  '#1976D2', '#388E3C', '#F57C00', '#D32F2F', '#7B1FA2'
]

/**
 * 默认看板列
 */
export const DEFAULT_KANBAN_COLUMNS = [
  { name: '待处理', position: 0 },
  { name: '进行中', position: 1 },
  { name: '已完成', position: 2 }
]
