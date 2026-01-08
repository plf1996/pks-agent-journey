<template>
  <div class="tags-page">
    <div class="tags-page__header">
      <h2 class="tags-page__title">标签管理</h2>
      <el-button type="primary" :icon="Plus" @click="showCreateDialog">
        新建标签
      </el-button>
    </div>

    <el-row :gutter="20">
      <el-col :xs="24" :sm="24" :md="16" :lg="16" :xl="16">
        <el-card v-loading="tagsStore.loading">
          <div v-if="tagsStore.tags.length > 0" class="tags-list">
            <div
              v-for="tag in tagsStore.tags"
              :key="tag.id"
              class="tag-item"
              @click="viewTag(tag.id)"
            >
              <el-tag :color="tag.color" size="large" class="tag-item__tag">
                {{ tag.name }}
              </el-tag>
              <span class="tag-item__count">{{ tag.cards_count || 0 }} 张卡片</span>
              <el-dropdown trigger="click" @command="(cmd) => handleCommand(cmd, tag)">
                <el-icon class="tag-item__more" @click.stop>
                  <MoreFilled />
                </el-icon>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item command="edit">编辑</el-dropdown-item>
                    <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </div>
          <el-empty v-else description="暂无标签" />
        </el-card>
      </el-col>

      <el-col :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <el-card>
          <template #header>
            <span>标签统计</span>
          </template>
          <div class="tag-stats">
            <div class="tag-stat-item">
              <span class="tag-stat-label">总标签数</span>
              <span class="tag-stat-value">{{ tagsStore.tags.length }}</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 创建/编辑标签对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingTag ? '编辑标签' : '新建标签'"
      width="400px"
    >
      <el-form :model="tagForm" label-width="80px">
        <el-form-item label="标签名称">
          <el-input v-model="tagForm.name" placeholder="请输入标签名称" />
        </el-form-item>
        <el-form-item label="标签颜色">
          <el-color-picker v-model="tagForm.color" />
        </el-form-item>
        <el-form-item label="父标签">
          <el-select v-model="tagForm.parent_id" placeholder="选择父标签（可选）" clearable>
            <el-option
              v-for="tag in tagsStore.tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
              :disabled="editingTag && tag.id === editingTag.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSave">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useTagsStore } from '@/stores/tags'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, MoreFilled } from '@element-plus/icons-vue'

const router = useRouter()
const tagsStore = useTagsStore()

const dialogVisible = ref(false)
const editingTag = ref(null)
const tagForm = ref({
  name: '',
  color: '#409EFF',
  parent_id: null
})

onMounted(async () => {
  await tagsStore.fetchTags()
})

const showCreateDialog = () => {
  editingTag.value = null
  tagForm.value = {
    name: '',
    color: '#409EFF',
    parent_id: null
  }
  dialogVisible.value = true
}

const handleSave = async () => {
  if (!tagForm.value.name) {
    ElMessage.warning('请输入标签名称')
    return
  }

  try {
    if (editingTag.value) {
      await tagsStore.updateTag(editingTag.value.id, tagForm.value)
      ElMessage.success('更新成功')
    } else {
      await tagsStore.createTag(tagForm.value)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleCommand = async (command, tag) => {
  switch (command) {
    case 'edit':
      editTag(tag)
      break
    case 'delete':
      await deleteTag(tag)
      break
  }
}

const editTag = (tag) => {
  editingTag.value = tag
  tagForm.value = {
    name: tag.name,
    color: tag.color,
    parent_id: tag.parent_id
  }
  dialogVisible.value = true
}

const deleteTag = async (tag) => {
  try {
    await ElMessageBox.confirm(
      `确定要删除标签"${tag.name}"吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await tagsStore.deleteTag(tag.id)
    ElMessage.success('删除成功')
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const viewTag = (tagId) => {
  router.push({ path: '/cards', query: { tag_id: tagId } })
}
</script>

<style scoped>
.tags-page {
  padding: 0;
}

.tags-page__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.tags-page__title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.tags-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.tag-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s;
}

.tag-item:hover {
  background-color: #f5f7fa;
  border-color: #409EFF;
}

.tag-item__tag {
  flex: 1;
}

.tag-item__count {
  font-size: 12px;
  color: #909399;
}

.tag-item__more {
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.tag-item__more:hover {
  background-color: #e4e7ed;
}

.tag-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tag-stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.tag-stat-label {
  font-size: 14px;
  color: #606266;
}

.tag-stat-value {
  font-size: 20px;
  font-weight: bold;
  color: #409EFF;
}
</style>
