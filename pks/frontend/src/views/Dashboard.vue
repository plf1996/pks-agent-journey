<template>
  <div class="dashboard">
    <h2 class="dashboard__title">仪表盘</h2>

    <el-row :gutter="20" class="dashboard__stats">
      <el-col :xs="12" :sm="6" :md="6" :lg="6" :xl="6">
        <el-card class="stat-card">
          <div class="stat-card__content">
            <el-icon class="stat-card__icon" color="#409EFF" :size="32">
              <Document />
            </el-icon>
            <div class="stat-card__info">
              <p class="stat-card__value">{{ stats.totalCards }}</p>
              <p class="stat-card__label">总卡片数</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="12" :sm="6" :md="6" :lg="6" :xl="6">
        <el-card class="stat-card">
          <div class="stat-card__content">
            <el-icon class="stat-card__icon" color="#67C23A" :size="32">
              <PriceTag />
            </el-icon>
            <div class="stat-card__info">
              <p class="stat-card__value">{{ stats.totalTags }}</p>
              <p class="stat-card__label">标签数</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="12" :sm="6" :md="6" :lg="6" :xl="6">
        <el-card class="stat-card">
          <div class="stat-card__content">
            <el-icon class="stat-card__icon" color="#E6A23C" :size="32">
              <Link />
            </el-icon>
            <div class="stat-card__info">
              <p class="stat-card__value">{{ stats.totalLinks }}</p>
              <p class="stat-card__label">链接数</p>
            </div>
          </div>
        </el-card>
      </el-col>

      <el-col :xs="12" :sm="6" :md="6" :lg="6" :xl="6">
        <el-card class="stat-card">
          <div class="stat-card__content">
            <el-icon class="stat-card__icon" color="#F56C6C" :size="32">
              <View />
            </el-icon>
            <div class="stat-card__info">
              <p class="stat-card__value">{{ stats.totalViews }}</p>
              <p class="stat-card__label">总浏览量</p>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="dashboard__content">
      <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
        <el-card class="dashboard-card">
          <template #header>
            <div class="card-header">
              <span>最近创建的卡片</span>
              <router-link to="/cards" class="more-link">查看更多</router-link>
            </div>
          </template>
          <div v-if="recentCards.length > 0" class="card-list">
            <div
              v-for="card in recentCards"
              :key="card.id"
              class="card-item"
              @click="goToCard(card.id)"
            >
              <div class="card-item__icon">
                <el-icon :color="getCardTypeColor(card.card_type)">
                  <component :is="getCardTypeIcon(card.card_type)" />
                </el-icon>
              </div>
              <div class="card-item__content">
                <h4 class="card-item__title">{{ card.title }}</h4>
                <p class="card-item__summary">{{ truncateText(card.content, 100) }}</p>
                <div class="card-item__meta">
                  <span class="card-item__time">{{ formatRelativeTime(card.created_at) }}</span>
                  <el-tag
                    v-for="tag in card.tags?.slice(0, 3)"
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
          <el-empty v-else description="暂无卡片" />
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <el-card class="dashboard-card">
          <template #header>
            <div class="card-header">
              <span>常用标签</span>
              <router-link to="/tags" class="more-link">查看更多</router-link>
            </div>
          </template>
          <div v-if="popularTags.length > 0" class="tag-cloud">
            <el-tag
              v-for="tag in popularTags"
              :key="tag.id"
              :color="tag.color"
              class="tag-cloud-item"
              @click="filterByTag(tag.id)"
            >
              {{ tag.name }} ({{ tag.cards_count || 0 }})
            </el-tag>
          </div>
          <el-empty v-else description="暂无标签" />
        </el-card>

        <el-card class="dashboard-card">
          <template #header>
            <span>快速操作</span>
          </template>
          <div class="quick-actions">
            <el-button type="primary" :icon="Plus" @click="createNewCard">
              新建卡片
            </el-button>
            <el-button :icon="Search" @click="goToSearch">
              全局搜索
            </el-button>
            <el-button :icon="Grid" @click="goToKanban">
              看板视图
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useCardsStore } from '@/stores/cards'
import { useTagsStore } from '@/stores/tags'
import { CARD_TYPES, CARD_TYPE_OPTIONS } from '@/utils/constants'
import { formatRelativeTime, truncateText } from '@/utils/format'
import {
  Document,
  PriceTag,
  Link,
  View,
  Plus,
  Search,
  Grid
} from '@element-plus/icons-vue'

const router = useRouter()
const cardsStore = useCardsStore()
const tagsStore = useTagsStore()

const stats = ref({
  totalCards: 0,
  totalTags: 0,
  totalLinks: 0,
  totalViews: 0
})

const recentCards = ref([])
const popularTags = ref([])

onMounted(async () => {
  await loadData()
})

const loadData = async () => {
  try {
    // 加载最近卡片
    const cardsData = await cardsStore.fetchCards({
      page: 1,
      page_size: 5,
      sort_by: 'created_at',
      order: 'desc'
    })
    recentCards.value = cardsData?.items || []

    // 加载标签
    const tagsData = await tagsStore.fetchTags()
    popularTags.value = tagsData?.items?.slice(0, 10) || []

    // 更新统计数据
    stats.value = {
      totalCards: cardsData?.total || 0,
      totalTags: tagsData?.total || 0,
      totalLinks: 0, // 这里需要API支持
      totalViews: recentCards.value.reduce((sum, card) => sum + (card.view_count || 0), 0)
    }
  } catch (error) {
    console.error('加载数据失败:', error)
  }
}

const goToCard = (cardId) => {
  router.push(`/cards/${cardId}`)
}

const filterByTag = (tagId) => {
  router.push({ path: '/cards', query: { tag_id: tagId } })
}

const createNewCard = () => {
  router.push('/cards/new')
}

const goToSearch = () => {
  router.push('/search')
}

const goToKanban = () => {
  router.push('/kanban')
}

const getCardTypeIcon = (type) => {
  const option = CARD_TYPE_OPTIONS.find(opt => opt.value === type)
  return option?.icon || 'Document'
}

const getCardTypeColor = (type) => {
  const colors = {
    [CARD_TYPES.NOTE]: '#409EFF',
    [CARD_TYPES.LINK]: '#67C23A',
    [CARD_TYPES.IMAGE]: '#E6A23C',
    [CARD_TYPES.CODE]: '#F56C6C'
  }
  return colors[type] || '#909399'
}
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.dashboard__title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 20px;
  color: #303133;
}

.dashboard__stats {
  margin-bottom: 20px;
}

.stat-card {
  margin-bottom: 20px;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.stat-card__content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-card__icon {
  flex-shrink: 0;
}

.stat-card__info {
  flex: 1;
}

.stat-card__value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin: 0 0 4px 0;
}

.stat-card__label {
  font-size: 14px;
  color: #909399;
  margin: 0;
}

.dashboard__content {
  margin-top: 20px;
}

.dashboard-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.more-link {
  color: #409EFF;
  text-decoration: none;
  font-size: 14px;
}

.more-link:hover {
  text-decoration: underline;
}

.card-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card-item {
  display: flex;
  gap: 12px;
  padding: 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.card-item:hover {
  background-color: #f5f7fa;
}

.card-item__icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.card-item__content {
  flex: 1;
  min-width: 0;
}

.card-item__title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 4px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-item__summary {
  font-size: 14px;
  color: #606266;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.card-item__meta {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.card-item__time {
  font-size: 12px;
  color: #909399;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-cloud-item {
  cursor: pointer;
  transition: all 0.3s;
}

.tag-cloud-item:hover {
  transform: scale(1.05);
}

.quick-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.quick-actions .el-button {
  width: 100%;
  justify-content: flex-start;
}

@media (max-width: 768px) {
  .dashboard__stats {
    margin-bottom: 10px;
  }

  .stat-card {
    margin-bottom: 10px;
  }

  .stat-card__value {
    font-size: 24px;
  }
}
</style>
