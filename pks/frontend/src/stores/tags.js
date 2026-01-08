import { defineStore } from 'pinia'
import { getTags, createTag, updateTag, deleteTag } from '@/api/tags'

export const useTagsStore = defineStore('tags', {
  state: () => ({
    tags: [],
    tagTree: [],
    currentTag: null,
    loading: false
  }),

  getters: {
    // 获取所有根标签
    rootTags: (state) => state.tags.filter(tag => !tag.parent_id),

    // 按父标签 ID 获取子标签
    childTags: (state) => (parentId) =>
      state.tags.filter(tag => tag.parent_id === parentId),

    // 获取标签名称映射
    tagMap: (state) => {
      const map = new Map()
      state.tags.forEach(tag => {
        map.set(tag.id, tag)
      })
      return map
    }
  },

  actions: {
    // 获取标签列表
    async fetchTags(params = {}) {
      this.loading = true
      try {
        const data = await getTags(params)
        this.tags = data.items || []

        // 构建标签树
        this.buildTagTree()

        return data
      } catch (error) {
        console.error('获取标签列表失败:', error)
        throw error
      } finally {
        this.loading = false
      }
    },

    // 创建标签
    async createTag(tagData) {
      try {
        const tag = await createTag(tagData)
        this.tags.push(tag)
        this.buildTagTree()
        return tag
      } catch (error) {
        console.error('创建标签失败:', error)
        throw error
      }
    },

    // 更新标签
    async updateTag(tagId, tagData) {
      try {
        const updatedTag = await updateTag(tagId, tagData)

        // 更新列表中的标签
        const index = this.tags.findIndex(tag => tag.id === tagId)
        if (index !== -1) {
          this.tags[index] = updatedTag
        }

        this.buildTagTree()
        return updatedTag
      } catch (error) {
        console.error('更新标签失败:', error)
        throw error
      }
    },

    // 删除标签
    async deleteTag(tagId) {
      try {
        await deleteTag(tagId)

        // 从列表中移除
        this.tags = this.tags.filter(tag => tag.id !== tagId)
        this.buildTagTree()
      } catch (error) {
        console.error('删除标签失败:', error)
        throw error
      }
    },

    // 构建标签树
    buildTagTree() {
      const buildTree = (parentId = null) => {
        return this.tags
          .filter(tag => tag.parent_id === parentId)
          .map(tag => ({
            ...tag,
            children: buildTree(tag.id)
          }))
      }

      this.tagTree = buildTree()
    },

    // 根据 ID 获取标签
    getTagById(tagId) {
      return this.tags.find(tag => tag.id === tagId)
    }
  }
})
