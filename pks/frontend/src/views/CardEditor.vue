<template>
  <div class="card-editor-page">
    <div class="card-editor-page__header">
      <h2 class="card-editor-page__title">
        {{ isEdit ? '编辑卡片' : '新建卡片' }}
      </h2>
      <div class="card-editor-page__actions">
        <el-button @click="goBack">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">
          保存
        </el-button>
      </div>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      class="card-editor-form"
    >
      <el-card class="form-card">
        <el-form-item label="卡片标题" prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入卡片标题"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="卡片类型" prop="card_type">
          <el-radio-group v-model="form.card_type">
            <el-radio
              v-for="type in CARD_TYPE_OPTIONS"
              :key="type.value"
              :label="type.value"
            >
              <el-icon><component :is="type.icon" /></el-icon>
              {{ type.label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>

        <el-form-item v-if="form.card_type === 'link'" label="网页链接" prop="url">
          <el-input
            v-model="form.url"
            placeholder="请输入网页链接"
            type="url"
          />
        </el-form-item>

        <el-form-item label="卡片内容" prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :placeholder="getContentPlaceholder()"
            :rows="10"
            maxlength="10000"
            show-word-limit
          />
        </el-form-item>

        <el-form-item label="标签">
          <el-select
            v-model="form.tag_ids"
            multiple
            placeholder="选择标签"
            filterable
            allow-create
            style="width: 100%"
          >
            <el-option
              v-for="tag in tagsStore.tags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            >
              <span>{{ tag.name }}</span>
              <span style="float: right; color: #8492a6; font-size: 12px">
                <el-color-picker :model-value="tag.color" size="small" disabled />
              </span>
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="关联卡片">
          <el-select
            v-model="form.link_ids"
            multiple
            placeholder="选择要关联的卡片"
            filterable
            style="width: 100%"
          >
            <el-option
              v-for="card in availableCards"
              :key="card.id"
              :label="card.title"
              :value="card.id"
              :disabled="card.id === currentCardId"
            />
          </el-select>
          <div class="form-tip">
            <el-icon><InfoFilled /></el-icon>
            创建双向链接，两张卡片会相互关联
          </div>
        </el-form-item>

        <el-form-item label="置顶">
          <el-switch v-model="form.is_pinned" />
        </el-form-item>
      </el-card>
    </el-form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useCardsStore } from '@/stores/cards'
import { useTagsStore } from '@/stores/tags'
import { CARD_TYPE_OPTIONS } from '@/utils/constants'
import { ElMessage } from 'element-plus'
import { InfoFilled } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const cardsStore = useCardsStore()
const tagsStore = useTagsStore()

const formRef = ref(null)
const saving = ref(false)
const availableCards = ref([])

const isEdit = computed(() => !!route.params.id)
const currentCardId = computed(() => {
  const id = route.params.id
  return id ? parseInt(id) : null
})

const form = reactive({
  title: '',
  content: '',
  card_type: 'note',
  url: '',
  tag_ids: [],
  link_ids: [],
  is_pinned: false
})

const rules = {
  title: [
    { required: true, message: '请输入卡片标题', trigger: 'blur' },
    { min: 1, max: 200, message: '标题长度在 1 到 200 个字符', trigger: 'blur' }
  ],
  card_type: [
    { required: true, message: '请选择卡片类型', trigger: 'change' }
  ],
  content: [
    { required: true, message: '请输入卡片内容', trigger: 'blur' }
  ],
  url: [
    {
      validator: (rule, value, callback) => {
        if (form.card_type === 'link' && !value) {
          callback(new Error('链接类型卡片必须填写网页链接'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

onMounted(async () => {
  await Promise.all([
    tagsStore.fetchTags(),
    loadAvailableCards()
  ])

  if (isEdit.value) {
    await loadCard()
  }
})

const loadCard = async () => {
  try {
    const card = await cardsStore.fetchCardDetail(currentCardId.value)

    form.title = card.title
    form.content = card.content
    form.card_type = card.card_type
    form.url = card.url || ''
    form.is_pinned = card.is_pinned || false

    // 设置标签
    form.tag_ids = card.tags?.map(tag => tag.id) || []

    // 设置关联卡片
    form.link_ids = card.links?.outgoing?.map(link => link.id) || []
  } catch (error) {
    ElMessage.error('加载卡片失败')
    router.back()
  }
}

const loadAvailableCards = async () => {
  try {
    const data = await cardsStore.fetchCards({
      page: 1,
      page_size: 100
    })
    availableCards.value = data?.items || []
  } catch (error) {
    console.error('加载卡片列表失败:', error)
  }
}

const getContentPlaceholder = () => {
  const placeholders = {
    note: '请输入笔记内容，支持 Markdown 格式',
    link: '请输入关于该链接的描述或笔记',
    image: '请输入图片描述或备注',
    code: '请输入代码内容'
  }
  return placeholders[form.card_type] || '请输入内容'
}

const handleSave = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    saving.value = true

    const data = {
      title: form.title,
      content: form.content,
      card_type: form.card_type,
      url: form.card_type === 'link' ? form.url : null,
      is_pinned: form.is_pinned,
      tag_ids: form.tag_ids,
      link_ids: form.link_ids
    }

    if (isEdit.value) {
      await cardsStore.updateCard(currentCardId.value, data)
      ElMessage.success('更新成功')
    } else {
      const card = await cardsStore.createCard(data)
      ElMessage.success('创建成功')
      router.push(`/cards/${card.id}`)
      return
    }

    router.back()
  } catch (error) {
    if (error.message) {
      ElMessage.error(error.message)
    }
  } finally {
    saving.value = false
  }
}

const goBack = () => {
  router.back()
}
</script>

<style scoped>
.card-editor-page {
  padding: 0;
}

.card-editor-page__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-editor-page__title {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

.card-editor-page__actions {
  display: flex;
  gap: 12px;
}

.form-card {
  max-width: 900px;
}

.form-tip {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .card-editor-page__header {
    flex-direction: column;
    gap: 12px;
    align-items: stretch;
  }

  .form-card :deep(.el-form-item__label) {
    width: 80px !important;
  }
}
</style>
