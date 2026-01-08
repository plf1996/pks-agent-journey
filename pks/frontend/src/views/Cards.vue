<template>
  <div class="cards-page">
    <div class="cards-page__header">
      <h2 class="cards-page__title">卡片管理</h2>
      <el-button type="primary" :icon="Plus" @click="handleNewCard">
        新建卡片
      </el-button>
    </div>

    <el-card class="filter-card">
      <el-form :inline="true" :model="filters" @submit.prevent="handleSearch">
        <el-form-item label="搜索">
          <el-input
            v-model="filters.search"
            placeholder="搜索标题或内容"
            clearable
            @keyup.enter="handleSearch"
          />
        </el-form-item>

        <el-form-item label="类型">
          <el-select
            v-model="filters.card_type"
            placeholder="全部类型"
            clearable
            @change="handleSearch"
          >
            <el-option
              v-for="type in CARD_TYPE_OPTIONS"
              :key="type.value"
              :label="type.label"
              :value="type.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="标签">
          <el-select
            v-model="filters.tag_id"
            placeholder="全部标签"
            clearable
            filterable
            @change="handleSearch"
          >
            <el-option
              v-for="tag in tagsStore.tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="排序">
          <el-select
            v-model="filters.sort_by"
            @change="handleSearch"
          >
            <el-option
              v-for="option in SORT_OPTIONS"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            搜索
          </el-button>
          <el-button @click="handleReset">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <div v-loading="cardsStore.loading" class="cards-list">
      <div v-if="cardsStore.cards.length > 0">
        <el-row :gutter="20">
          <el-col
            v-for="card in cardsStore.cards"
            :key="card.id"
            :xs="24"
            :sm="12"
            :md="8"
            :lg="6"
            :xl="6"
          >
            <el-card class="card-item" @click="goToCard(card.id)">
              <div class="card-item__header">
                <el-tag :color="getCardTypeColor(card.card_type)" size="small">
                  {{ getCardTypeLabel(card.card_type) }}
                </el-tag>
                <el-dropdown trigger="click" @command="(cmd) => handleCardAction(cmd, card)">
                  <el-icon class="card-item__more" @click.stop>
                    <MoreFilled />
                  </el-icon>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item command="edit" @click.stop="editCard(card.id)">
                        编辑
                      </el-dropdown-item>
                      <el-dropdown-item command="delete" @click.stop="deleteCard(card.id)">
                        删除
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>

              <h3 class="card-item__title">{{ card.title }}</h3>
              <p class="card-item__content">{{ truncateText(card.content, 100) }}</p>

              <div v-if="card.url" class="card-item__url">
                <el-icon><Link /></el-icon>
                <span>{{ truncateText(card.url, 50) }}</span>
              </div>

              <div v-if="card.tags?.length > 0" class="card-item__tags">
                <el-tag
                  v-for="tag in card.tags.slice(0, 3)"
                  :key="tag.id"
                  size="small"
                  :color="tag.color"
                >
                  {{ tag.name }}
                </el-tag>
              </div>

              <div class="card-item__footer">
                <span class="card-item__time">{{ formatRelativeTime(card.created_at) }}</span>
                <span class="card-item__views">
                  <el-icon><View /></el-icon>
                  {{ card.view_count || 0 }}
                </span>
              </div>
            </el-card>
          </el-col>
        </el-row>

        <el-pagination
          v-if="cardsStore.total > 0"
          class="pagination"
          :current-page="cardsStore.currentPage"
          :page-size="cardsStore.pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="cardsStore.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>

      <el-empty v-else description="暂无卡片" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCardsStore } from '@/stores/cards'
import { useTagsStore } from '@/stores/tags'
import { CARD_TYPE_OPTIONS, SORT_OPTIONS } from '@/utils/constants'
import { formatRelativeTime, truncateText } from '@/utils/format'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  MoreFilled,
  Link,
  View
} from '@element-plus/icons-vue'

const router = useRouter()
const cardsStore = useCardsStore()
const tagsStore = useTagsStore()

const filters = ref({
  search: '',
  card_type: '',
  tag_id: null,
  sort_by: 'created_at'
})

onMounted(async () => {
  await Promise.all([
    loadCards(),
    tagsStore.fetchTags()
  ])
})

// 监听路由查询参数变化
watch(() => router.currentRoute.value.query, async (newQuery) => {
  if (router.currentRoute.value.name === 'Cards') {
    if (newQuery.tag_id) {
      filters.value.tag_id = parseInt(newQuery.tag_id)
    }
    await loadCards()
  }
}, { immediate: true })

const loadCards = async () => {
  try {
    await cardsStore.fetchCards(filters.value)
  } catch (error) {
    ElMessage.error('加载卡片列表失败')
  }
}

const handleSearch = () => {
  cardsStore.currentPage = 1
  loadCards()
}

const handleReset = () => {
  filters.value = {
    search: '',
    card_type: '',
    tag_id: null,
    sort_by: 'created_at'
  }
  cardsStore.resetFilters()
  loadCards()
}

const handlePageChange = (page) => {
  cardsStore.currentPage = page
  loadCards()
}

const handleSizeChange = (size) => {
  cardsStore.pageSize = size
  cardsStore.currentPage = 1
  loadCards()
}

const handleNewCard = () => {
  router.push('/cards/new')
}

const goToCard = (cardId) => {
  router.push(`/cards/${cardId}`)
}

const editCard = (cardId) => {
  router.push(`/cards/${cardId}/edit`)
}

const deleteCard = async (cardId) => {
  try {
    await ElMessageBox.confirm('确定要删除这张卡片吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    await cardsStore.deleteCard(cardId)
    ElMessage.success('删除成功')
    await loadCards()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleCardAction = (command, card) => {
  switch (command) {
    case 'edit':
      editCard(card.id)
      break
    case 'delete':
      deleteCard(card.id)
      break
  }
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
.cards-page {
  padding: 0;
}

.cards-page__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.cards-page__title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.filter-card {
  margin-bottom: 20px;
}

.cards-list {
  min-height: 400px;
}

.card-item {
  height: 100%;
  cursor: pointer;
  transition: all 0.3s;
  margin-bottom: 20px;
}

.card-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.card-item__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.card-item__more {
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.card-item__more:hover {
  background-color: #f5f7fa;
}

.card-item__title {
  font-size: 18px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-item__content {
  font-size: 14px;
  color: #606266;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  min-height: 60px;
}

.card-item__url {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #409EFF;
  margin-bottom: 12px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.card-item__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 12px;
}

.card-item__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #909399;
}

.card-item__time {
  flex: 1;
}

.card-item__views {
  display: flex;
  align-items: center;
  gap: 4px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .cards-page__header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .filter-card :deep(.el-form) {
    flex-direction: column;
  }

  .filter-card :deep(.el-form-item) {
    width: 100%;
    margin-right: 0;
  }
}
</style>
