<template>
  <div v-loading="loading" class="card-detail-page">
    <div v-if="card" class="card-detail">
      <div class="card-detail__header">
        <div class="card-detail__back">
          <el-button :icon="ArrowLeft" @click="goBack">返回</el-button>
        </div>
        <div class="card-detail__actions">
          <el-button :icon="Edit" @click="editCard">编辑</el-button>
          <el-button type="danger" :icon="Delete" @click="deleteCard">删除</el-button>
        </div>
      </div>

      <el-card class="card-content">
        <div class="card-content__meta">
          <el-tag :color="getCardTypeColor(card.card_type)">
            {{ getCardTypeLabel(card.card_type) }}
          </el-tag>
          <span class="card-content__time">
            {{ formatDateTime(card.created_at) }}
          </span>
          <span class="card-content__views">
            <el-icon><View /></el-icon>
            {{ card.view_count || 0 }} 次浏览
          </span>
        </div>

        <h1 class="card-content__title">{{ card.title }}</h1>

        <div v-if="card.url" class="card-content__url">
          <el-icon><Link /></el-icon>
          <a :href="card.url" target="_blank" rel="noopener">{{ card.url }}</a>
        </div>

        <div class="card-content__body">
          <div v-if="card.card_type === 'code'" class="code-block">
            <pre><code>{{ card.content }}</code></pre>
          </div>
          <div v-else class="markdown-content" v-html="renderMarkdown(card.content)" />
        </div>

        <div v-if="card.tags?.length > 0" class="card-content__tags">
          <span class="tags-label">标签：</span>
          <el-tag
            v-for="tag in card.tags"
            :key="tag.id"
            :color="tag.color"
            class="tag-item"
            @click="filterByTag(tag.id)"
          >
            {{ tag.name }}
          </el-tag>
        </div>

        <!-- 双向链接 -->
        <div v-if="hasLinks" class="card-links">
          <div v-if="card.links?.outgoing?.length > 0" class="links-section">
            <h3 class="links-section__title">引用的卡片</h3>
            <div class="links-list">
              <div
                v-for="link in card.links.outgoing"
                :key="link.id"
                class="link-item"
                @click="goToCard(link.id)"
              >
                <el-icon><Link /></el-icon>
                <span>{{ link.title }}</span>
                <el-tag size="small">{{ getLinkTypeLabel(link.link_type) }}</el-tag>
              </div>
            </div>
          </div>

          <div v-if="card.links?.incoming?.length > 0" class="links-section">
            <h3 class="links-section__title">被引用的卡片</h3>
            <div class="links-list">
              <div
                v-for="link in card.links.incoming"
                :key="link.id"
                class="link-item"
                @click="goToCard(link.id)"
              >
                <el-icon><Link /></el-icon>
                <span>{{ link.title }}</span>
                <el-tag size="small">{{ getLinkTypeLabel(link.link_type) }}</el-tag>
              </div>
            </div>
          </div>
        </div>
      </el-card>
    </div>

    <el-empty v-else description="卡片不存在" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { getCardDetail, deleteCard as deleteCardApi } from '@/api/cards'
import { CARD_TYPE_OPTIONS, LINK_TYPES } from '@/utils/constants'
import { formatDateTime } from '@/utils/format'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ArrowLeft,
  Edit,
  Delete,
  View,
  Link
} from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const loading = ref(false)
const card = ref(null)

const hasLinks = computed(() => {
  return (card.value?.links?.outgoing?.length > 0) || (card.value?.links?.incoming?.length > 0)
})

onMounted(async () => {
  await loadCard()
})

const loadCard = async () => {
  loading.value = true
  try {
    const cardId = route.params.id
    card.value = await getCardDetail(cardId)
  } catch (error) {
    ElMessage.error('加载卡片失败')
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.back()
}

const editCard = () => {
  router.push(`/cards/${card.value.id}/edit`)
}

const deleteCard = async () => {
  try {
    await ElMessageBox.confirm('确定要删除这张卡片吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await deleteCardApi(card.value.id)
    ElMessage.success('删除成功')
    router.push('/cards')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const goToCard = (cardId) => {
  router.push(`/cards/${cardId}`)
}

const filterByTag = (tagId) => {
  router.push({ path: '/cards', query: { tag_id: tagId } })
}

const getCardTypeLabel = (type) => {
  const option = CARD_TYPE_OPTIONS.find(opt => opt.value === type)
  return option?.label || '未知'
}

const getCardTypeColor = (type) => {
  const colors = {
    note: '#409EFF',
    link: '#67C23A',
    image: '#E6A23C',
    code: '#F56C6C'
  }
  return colors[type] || '#909399'
}

const getLinkTypeLabel = (type) => {
  const labels = {
    [LINK_TYPES.REFERENCE]: '引用',
    [LINK_TYPES.RELATED]: '相关',
    [LINK_TYPES.PARENT]: '父级'
  }
  return labels[type] || '未知'
}

const renderMarkdown = (content) => {
  // 简单的 Markdown 渲染（生产环境建议使用 marked 或 markdown-it）
  if (!content) return ''

  return content
    .replace(/^### (.*$)/gim, '<h3>$1</h3>')
    .replace(/^## (.*$)/gim, '<h2>$1</h2>')
    .replace(/^# (.*$)/gim, '<h1>$1</h1>')
    .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
    .replace(/\*(.*)\*/gim, '<em>$1</em>')
    .replace(/\n/gim, '<br>')
}
</script>

<style scoped>
.card-detail-page {
  padding: 0;
}

.card-detail {
  max-width: 900px;
  margin: 0 auto;
}

.card-detail__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-detail__actions {
  display: flex;
  gap: 12px;
}

.card-content {
  margin-bottom: 20px;
}

.card-content__meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
  font-size: 14px;
  color: #909399;
}

.card-content__title {
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 20px 0;
  line-height: 1.4;
}

.card-content__url {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 20px;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.card-content__url a {
  color: #409EFF;
  text-decoration: none;
  word-break: break-all;
}

.card-content__url a:hover {
  text-decoration: underline;
}

.card-content__body {
  margin-bottom: 24px;
}

.code-block {
  background-color: #f5f7fa;
  border-radius: 4px;
  padding: 16px;
  overflow-x: auto;
}

.code-block pre {
  margin: 0;
}

.code-block code {
  font-family: 'Courier New', Courier, monospace;
  font-size: 14px;
  line-height: 1.6;
  color: #303133;
}

.markdown-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
}

.markdown-content :deep(h1),
.markdown-content :deep(h2),
.markdown-content :deep(h3) {
  margin-top: 24px;
  margin-bottom: 16px;
  font-weight: 600;
  line-height: 1.4;
}

.markdown-content :deep(h1) {
  font-size: 24px;
}

.markdown-content :deep(h2) {
  font-size: 20px;
}

.markdown-content :deep(h3) {
  font-size: 18px;
}

.markdown-content :deep(p) {
  margin-bottom: 16px;
}

.card-content__tags {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  padding: 16px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.tags-label {
  font-size: 14px;
  font-weight: 500;
  color: #606266;
}

.tag-item {
  cursor: pointer;
}

.card-links {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #e4e7ed;
}

.links-section {
  margin-bottom: 24px;
}

.links-section:last-child {
  margin-bottom: 0;
}

.links-section__title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 12px 0;
}

.links-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.link-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.link-item:hover {
  background-color: #e4e7ed;
}

@media (max-width: 768px) {
  .card-detail__header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .card-content__title {
    font-size: 24px;
  }
}
</style>
