<template>
  <div class="search-page">
    <div class="search-page__header">
      <h2 class="search-page__title">全局搜索</h2>
    </div>

    <el-card class="search-card">
      <el-input
        v-model="searchQuery"
        size="large"
        placeholder="输入关键词搜索卡片和标签..."
        :prefix-icon="Search"
        clearable
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button :icon="Search" @click="handleSearch">搜索</el-button>
        </template>
      </el-input>

      <div class="search-filters">
        <el-radio-group v-model="searchType" @change="handleSearch">
          <el-radio-button label="all">全部</el-radio-button>
          <el-radio-button label="cards">卡片</el-radio-button>
          <el-radio-button label="tags">标签</el-radio-button>
        </el-radio-group>
      </div>
    </el-card>

    <div v-loading="loading" class="search-results">
      <div v-if="hasResults" class="search-results__content">
        <!-- 卡片结果 -->
        <div v-if="results.cards?.items?.length > 0" class="result-section">
          <h3 class="result-section__title">
            <el-icon><Document /></el-icon>
            卡片 ({{ results.cards.total }})
          </h3>
          <div class="result-list">
            <div
              v-for="card in results.cards.items"
              :key="card.id"
              class="result-item"
              @click="goToCard(card.id)"
            >
              <div class="result-item__header">
                <h4 class="result-item__title" v-html="highlightText(card.title, searchQuery)" />
                <el-tag :color="getCardTypeColor(card.card_type)" size="small">
                  {{ getCardTypeLabel(card.card_type) }}
                </el-tag>
              </div>
              <p class="result-item__content" v-html="highlightText(card.content, searchQuery)" />
              <div class="result-item__meta">
                <span class="result-item__time">{{ formatRelativeTime(card.created_at) }}</span>
                <div v-if="card.tags?.length > 0" class="result-item__tags">
                  <el-tag
                    v-for="tag in card.tags.slice(0, 3)"
                    :key="tag.id"
                    size="small"
                    :color="tag.color"
                  >
                    {{ tag.name }}
                  </el-tag>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 标签结果 -->
        <div v-if="results.tags?.items?.length > 0" class="result-section">
          <h3 class="result-section__title">
            <el-icon><PriceTag /></el-icon>
            标签 ({{ results.tags.total }})
          </h3>
          <div class="result-list">
            <div
              v-for="tag in results.tags.items"
              :key="tag.id"
              class="result-item result-item--tag"
              @click="filterByTag(tag.id)"
            >
              <el-tag :color="tag.color" size="large">{{ tag.name }}</el-tag>
              <span class="tag-cards-count">{{ tag.cards_count || 0 }} 张卡片</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 无结果 -->
      <el-empty
        v-else-if="searched"
        description="未找到相关结果"
      >
        <template #image>
          <el-icon :size="100" color="#909399">
            <Search />
          </el-icon>
        </template>
      </el-empty>

      <!-- 未搜索 -->
      <el-empty
        v-else
        description="输入关键词开始搜索"
      >
        <template #image>
          <el-icon :size="100" color="#909399">
            <Search />
          </el-icon>
        </template>
      </el-empty>
    </div>

    <!-- 分页 -->
    <el-pagination
      v-if="hasResults && total > 0"
      class="pagination"
      :current-page="currentPage"
      :page-size="pageSize"
      :total="total"
      layout="prev, pager, next"
      @current-change="handlePageChange"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { search } from '@/api/search'
import { CARD_TYPE_OPTIONS } from '@/utils/constants'
import { formatRelativeTime } from '@/utils/format'
import { ElMessage } from 'element-plus'
import { Search, Document, PriceTag } from '@element-plus/icons-vue'

const router = useRouter()

const searchQuery = ref('')
const searchType = ref('all')
const loading = ref(false)
const searched = ref(false)
const results = ref({
  cards: { items: [], total: 0 },
  tags: { items: [], total: 0 }
})
const currentPage = ref(1)
const pageSize = ref(20)

const total = computed(() => {
  return (results.value.cards?.total || 0) + (results.value.tags?.total || 0)
})

const hasResults = computed(() => {
  return (results.value.cards?.items?.length > 0) || (results.value.tags?.items?.length > 0)
})

onMounted(() => {
  // 如果从路由查询参数中获取搜索关键词
  const query = router.currentRoute.value.query.q
  if (query) {
    searchQuery.value = query
    handleSearch()
  }
})

const handleSearch = async () => {
  if (!searchQuery.value.trim()) {
    ElMessage.warning('请输入搜索关键词')
    return
  }

  loading.value = true
  searched.value = true
  currentPage.value = 1

  try {
    const data = await search({
      q: searchQuery.value,
      type: searchType.value,
      page: currentPage.value,
      page_size: pageSize.value
    })

    results.value = data
  } catch (error) {
    ElMessage.error('搜索失败')
  } finally {
    loading.value = false
  }
}

const handlePageChange = async (page) => {
  currentPage.value = page
  await handleSearch()
}

const goToCard = (cardId) => {
  router.push(`/cards/${cardId}`)
}

const filterByTag = (tagId) => {
  router.push({ path: '/cards', query: { tag_id: tagId } })
}

const highlightText = (text, keyword) => {
  if (!text || !keyword) return text

  const regex = new RegExp(`(${keyword})`, 'gi')
  return text.replace(regex, '<mark>$1</mark>')
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
</script>

<style scoped>
.search-page {
  padding: 0;
}

.search-page__header {
  margin-bottom: 20px;
}

.search-page__title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.search-card {
  margin-bottom: 20px;
}

.search-filters {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

.search-results {
  min-height: 400px;
  margin-bottom: 20px;
}

.search-results__content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.result-section__title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 18px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 16px 0;
}

.result-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-item {
  background-color: white;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.result-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  border-color: #409EFF;
}

.result-item--tag {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
}

.result-item__header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
}

.result-item__title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin: 0;
  flex: 1;
}

.result-item__title :deep(mark) {
  background-color: #fffbdd;
  padding: 0 2px;
  border-radius: 2px;
}

.result-item__content {
  font-size: 14px;
  color: #606266;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.result-item__content :deep(mark) {
  background-color: #fffbdd;
  padding: 0 2px;
  border-radius: 2px;
}

.result-item__meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #909399;
}

.result-item__tags {
  display: flex;
  gap: 4px;
}

.tag-cards-count {
  font-size: 12px;
  color: #909399;
  margin-left: auto;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .search-card :deep(.el-input-group__append) {
    display: none;
  }

  .result-item__header {
    flex-direction: column;
    gap: 8px;
  }
}
</style>
