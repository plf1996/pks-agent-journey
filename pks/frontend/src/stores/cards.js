import { defineStore } from 'pinia'
import { getCards, getCardDetail, createCard, updateCard, deleteCard, batchDeleteCards } from '@/api/cards'

export const useCardsStore = defineStore('cards', {
  state: () => ({
    cards: [],
    currentCard: null,
    loading: false,
    total: 0,
    currentPage: 1,
    pageSize: 20,
    filters: {
      card_type: '',
      tag_id: null,
      is_pinned: false,
      search: '',
      sort_by: 'created_at',
      order: 'desc'
    }
  }),

  getters: {
    // 获取置顶卡片
    pinnedCards: (state) => state.cards.filter(card => card.is_pinned),

    // 获取普通卡片
    regularCards: (state) => state.cards.filter(card => !card.is_pinned),

    // 按类型筛选卡片
    cardsByType: (state) => (type) => state.cards.filter(card => card.card_type === type),

    // 按标签筛选卡片
    cardsByTag: (state) => (tagId) =>
      state.cards.filter(card => card.tags?.some(tag => tag.id === tagId))
  },

  actions: {
    // 获取卡片列表
    async fetchCards(params = {}) {
      this.loading = true
      try {
        const queryParams = {
          page: params.page || this.currentPage,
          page_size: params.page_size || this.pageSize,
          ...this.filters,
          ...params
        }

        const data = await getCards(queryParams)
        this.cards = data.items || []
        this.total = data.total || 0
        this.currentPage = data.page || 1

        return data
      } catch (error) {
        console.error('获取卡片列表失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 获取卡片详情
    async fetchCardDetail(cardId) {
      this.loading = true
      try {
        const card = await getCardDetail(cardId)
        this.currentCard = card
        return card
      } catch (error) {
        console.error('获取卡片详情失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 创建卡片
    async createCard(cardData) {
      try {
        const card = await createCard(cardData)
        this.cards.unshift(card)
        this.total++
        return card
      } catch (error) {
        console.error('创建卡片失败:', error)
        throw error
      }
    },

    // 更新卡片
    async updateCard(cardId, cardData) {
      try {
        const updatedCard = await updateCard(cardId, cardData)

        // 更新列表中的卡片
        const index = this.cards.findIndex(card => card.id === cardId)
        if (index !== -1) {
          this.cards[index] = updatedCard
        }

        // 更新当前卡片
        if (this.currentCard?.id === cardId) {
          this.currentCard = updatedCard
        }

        return updatedCard
      } catch (error) {
        console.error('更新卡片失败:', error)
        throw error
      }
    },

    // 删除卡片
    async deleteCard(cardId) {
      try {
        await deleteCard(cardId)

        // 从列表中移除
        this.cards = this.cards.filter(card => card.id !== cardId)
        this.total--

        // 清除当前卡片
        if (this.currentCard?.id === cardId) {
          this.currentCard = null
        }
      } catch (error) {
        console.error('删除卡片失败:', error)
        throw error
      }
    },

    // 批量删除卡片
    async batchDelete(cardIds) {
      try {
        await batchDeleteCards(cardIds)

        // 从列表中移除
        this.cards = this.cards.filter(card => !cardIds.includes(card.id))
        this.total -= cardIds.length
      } catch (error) {
        console.error('批量删除卡片失败:', error)
        throw error
      }
    },

    // 设置筛选条件
    setFilters(filters) {
      this.filters = { ...this.filters, ...filters }
      this.currentPage = 1
    },

    // 重置筛选条件
    resetFilters() {
      this.filters = {
        card_type: '',
        tag_id: null,
        is_pinned: false,
        search: '',
        sort_by: 'created_at',
        order: 'desc'
      }
      this.currentPage = 1
    },

    // 设置分页
    setPagination(page, pageSize) {
      this.currentPage = page
      if (pageSize) {
        this.pageSize = pageSize
      }
    }
  }
})
