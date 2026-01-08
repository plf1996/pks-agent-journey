<template>
  <footer class="footer">
    <div class="footer__container">
      <p class="footer__text">
        © {{ currentYear }} PKS - 个人知识管理系统
      </p>
      <p class="footer__description">
        一个简洁高效的知识管理工具，帮助你整理和管理碎片化信息
      </p>
    </div>
  </footer>
</template>

<script setup>
import { computed } from 'vue'

const currentYear = computed(() => new Date().getFullYear())
</script>

<style scoped>
.footer {
  background-color: #f5f7fa;
  border-top: 1px solid #e4e7ed;
  padding: 20px 0;
  margin-top: auto;
}

.footer__container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
  text-align: center;
}

.footer__text {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #606266;
}

.footer__description {
  margin: 0;
  font-size: 12px;
  color: #909399;
}

@media (max-width: 768px) {
  .footer__container {
    padding: 0 10px;
  }
}
</style>
