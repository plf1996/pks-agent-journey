<template>
  <div class="kanban-page">
    <div class="kanban-page__header">
      <h2 class="kanban-page__title">看板视图</h2>
      <el-button type="primary" :icon="Plus" @click="showAddColumnDialog">
        添加列
      </el-button>
    </div>

    <div v-loading="loading" class="kanban-board">
      <div
        v-for="column in columns"
        :key="column.id"
        class="kanban-column"
      >
        <div class="kanban-column__header">
          <h3 class="kanban-column__title">{{ column.name }}</h3>
          <el-dropdown trigger="click" @command="(cmd) => handleColumnCommand(cmd, column)">
            <el-icon class="kanban-column__more">
              <MoreFilled />
            </el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="edit">编辑列</el-dropdown-item>
                <el-dropdown-item command="delete" divided>删除列</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>

        <div class="kanban-column__content">
          <VueDraggable
            v-model="column.cards"
            class="kanban-cards"
            group="kanban"
            :animation="200"
            ghost-class="kanban-card-ghost"
            @end="handleDragEnd($event, column)"
          >
            <div
              v-for="card in column.cards"
              :key="card.id"
              class="kanban-card"
              @click="viewCard(card.id)"
            >
              <div class="kanban-card__type">
                <el-tag :color="getCardTypeColor(card.card_type)" size="small">
                  {{ getCardTypeLabel(card.card_type) }}
                </el-tag>
              </div>
              <h4 class="kanban-card__title">{{ card.title }}</h4>
              <p class="kanban-card__content">{{ truncateText(card.content, 80) }}</p>
              <div v-if="card.tags?.length > 0" class="kanban-card__tags">
                <el-tag
                  v-for="tag in card.tags.slice(0, 2)"
                  :key="tag.id"
                  size="small"
                  :color="tag.color"
                >
                  {{ tag.name }}
                </el-tag>
              </div>
            </div>
          </VueDraggable>

          <el-empty
            v-if="!column.cards || column.cards.length === 0"
            description="拖拽卡片到此处"
            :image-size="60"
          />
        </div>

        <div class="kanban-column__footer">
          <span class="card-count">{{ column.cards?.length || 0 }} 张卡片</span>
        </div>
      </div>
    </div>

    <!-- 添加/编辑列对话框 -->
    <el-dialog
      v-model="columnDialogVisible"
      :title="editingColumn ? '编辑列' : '添加列'"
      width="400px"
    >
      <el-form :model="columnForm" label-width="80px">
        <el-form-item label="列名称">
          <el-input v-model="columnForm.name" placeholder="请输入列名称" />
        </el-form-item>
        <el-form-item label="位置">
          <el-input-number v-model="columnForm.position" :min="0" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="columnDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSaveColumn">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { VueDraggable } from 'vue-draggable-plus'
import { getKanban, createKanbanColumn, updateKanbanColumn, deleteKanbanColumn, moveCardToColumn } from '@/api/kanban'
import { CARD_TYPE_OPTIONS } from '@/utils/constants'
import { truncateText } from '@/utils/format'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, MoreFilled } from '@element-plus/icons-vue'

const router = useRouter()

const loading = ref(false)
const columns = ref([])
const columnDialogVisible = ref(false)
const editingColumn = ref(null)
const columnForm = ref({
  name: '',
  position: 0
})

onMounted(async () => {
  await loadKanban()
})

const loadKanban = async () => {
  loading.value = true
  try {
    const data = await getKanban()
    columns.value = data.columns || []
  } catch (error) {
    ElMessage.error('加载看板失败')
  } finally {
    loading.value = false
  }
}

const showAddColumnDialog = () => {
  editingColumn.value = null
  columnForm.value = {
    name: '',
    position: columns.value.length
  }
  columnDialogVisible.value = true
}

const handleColumnCommand = async (command, column) => {
  switch (command) {
    case 'edit':
      editColumn(column)
      break
    case 'delete':
      await deleteColumn(column)
      break
  }
}

const editColumn = (column) => {
  editingColumn.value = column
  columnForm.value = {
    name: column.name,
    position: column.position
  }
  columnDialogVisible.value = true
}

const handleSaveColumn = async () => {
  try {
    if (editingColumn.value) {
      await updateKanbanColumn(editingColumn.value.id, columnForm.value)
      ElMessage.success('更新成功')
    } else {
      await createKanbanColumn(columnForm.value)
      ElMessage.success('创建成功')
    }
    columnDialogVisible.value = false
    await loadKanban()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteColumn = async (column) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除列"${column.name}"吗？列中的卡片将不会被删除。`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await deleteKanbanColumn(column.id)
    ElMessage.success('删除成功')
    await loadKanban()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleDragEnd = async (event, column) => {
  const { newIndex, item } = event
  const card = item.dataset

  if (newIndex === undefined || !card) return

  try {
    await moveCardToColumn({
      card_id: parseInt(card.id),
      column_id: column.id,
      position: newIndex
    })
  } catch (error) {
    ElMessage.error('移动失败')
    await loadKanban()
  }
}

const viewCard = (cardId) => {
  router.push(`/cards/${cardId}`)
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
.kanban-page {
  padding: 0;
}

.kanban-page__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.kanban-page__title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.kanban-board {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding-bottom: 20px;
  min-height: 600px;
}

.kanban-column {
  flex: 0 0 300px;
  background-color: #f5f7fa;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  max-height: calc(100vh - 200px);
}

.kanban-column__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
}

.kanban-column__title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
  margin: 0;
}

.kanban-column__more {
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.kanban-column__more:hover {
  background-color: #e4e7ed;
}

.kanban-column__content {
  flex: 1;
  overflow-y: auto;
  padding: 12px;
}

.kanban-cards {
  display: flex;
  flex-direction: column;
  gap: 12px;
  min-height: 100px;
}

.kanban-card {
  background-color: white;
  border-radius: 4px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.kanban-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.kanban-card-ghost {
  opacity: 0.5;
  background-color: #ecf5ff;
}

.kanban-card__type {
  margin-bottom: 8px;
}

.kanban-card__title {
  font-size: 14px;
  font-weight: 500;
  color: #303133;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.kanban-card__content {
  font-size: 12px;
  color: #606266;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}

.kanban-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.kanban-column__footer {
  padding: 12px 16px;
  border-top: 1px solid #e4e7ed;
  font-size: 12px;
  color: #909399;
}

.card-count {
  font-weight: 500;
}

@media (max-width: 768px) {
  .kanban-board {
    flex-direction: column;
    overflow-x: hidden;
  }

  .kanban-column {
    flex: 1;
    max-height: none;
  }
}
</style>
