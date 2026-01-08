<template>
  <div class="loading-spinner" v-if="visible">
    <div class="loading-spinner__spinner"></div>
    <p class="loading-spinner__text" v-if="text">{{ text }}</p>
  </div>
</template>

<script setup>
defineProps({
  visible: {
    type: Boolean,
    default: false
  },
  text: {
    type: String,
    default: '加载中...'
  }
})
</script>

<style scoped>
.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}

.loading-spinner__spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e4e7ed;
  border-top-color: #409EFF;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

.loading-spinner__text {
  margin-top: 16px;
  font-size: 14px;
  color: #909399;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
