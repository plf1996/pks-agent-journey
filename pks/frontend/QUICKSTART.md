# PKS 前端项目快速启动指南

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /root/projects/pks/frontend
npm install
```

### 2. 启动开发服务器

```bash
npm run dev
```

服务器将在 http://localhost:5173 启动

### 3. 访问应用

在浏览器中打开 http://localhost:5173

首次访问需要注册账号，然后登录即可使用。

## 📦 项目特性

### 已实现功能

1. **用户认证系统**
   - 用户注册
   - 用户登录
   - Token 持久化
   - 路由守卫

2. **卡片管理**
   - 创建卡片（笔记/链接/图片/代码）
   - 编辑卡片
   - 删除卡片
   - 卡片列表（分页、筛选）
   - 卡片详情查看
   - 批量删除

3. **标签系统**
   - 创建标签
   - 编辑标签
   - 删除标签
   - 标签筛选
   - 层级标签支持

4. **双向链接**
   - 关联卡片
   - 查看引用关系
   - 自动建立双向关系

5. **全局搜索**
   - 全文搜索
   - 关键词高亮
   - 分类搜索（卡片/标签）

6. **看板视图**
   - 创建看板列
   - 拖拽卡片
   - 自动保存位置

## 🏗️ 技术架构

### 前端技术栈
- Vue 3.4.21 (Composition API)
- Vite 5.2.0
- Vue Router 4.3.0
- Pinia 2.1.7
- Element Plus 2.7.0
- Axios 1.6.8
- Vue Draggable Plus 0.3.1

### 项目结构
```
frontend/
├── src/
│   ├── api/           # API 封装层
│   ├── components/    # Vue 组件
│   ├── views/         # 页面视图
│   ├── router/        # 路由配置
│   ├── stores/        # Pinia 状态管理
│   ├── composables/   # 组合式函数
│   ├── utils/         # 工具函数
│   └── assets/        # 静态资源
└── package.json
```

## 🔧 配置说明

### 环境变量

在 `.env` 文件中配置：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=个人知识管理系统
```

### API 配置

API 请求会自动：
- 添加 Authorization 头
- 处理响应统一格式
- 拦截错误并提示
- Token 过期自动跳转

## 📝 开发指南

### 添加新页面

1. 在 `src/views/` 创建页面组件
2. 在 `src/router/index.js` 添加路由
3. 在 Header.vue 添加导航链接

### 添加新 API

1. 在 `src/api/` 创建 API 文件
2. 使用 `request` 实例发送请求
3. 在组件中导入使用

### 状态管理

使用 Pinia Store：
- `authStore`: 认证状态
- `cardsStore`: 卡片数据
- `tagsStore`: 标签数据

## 🎨 UI 组件

使用 Element Plus 组件库：
- 按需引入已配置
- 图标自动注册
- 主题色可自定义

## 🔐 认证流程

1. 用户登录获取 Token
2. Token 存储在 localStorage
3. 每次 API 请求自动携带 Token
4. Token 过期自动跳转登录

## 📱 响应式设计

支持桌面端和移动端：
- 桌面端：完整功能
- 移动端：优化布局

## 🚨 错误处理

统一的错误处理机制：
- API 错误自动提示
- 表单验证提示
- 友好的错误信息

## 🎯 下一步计划

- [ ] 图片上传功能
- [ ] Markdown 编辑器增强
- [ ] 导出功能
- [ ] 快捷键支持
- [ ] 离线缓存
- [ ] PWA 支持

## 📚 相关文档

- [Vue 3 文档](https://cn.vuejs.org/)
- [Vite 文档](https://cn.vitejs.dev/)
- [Element Plus 文档](https://element-plus.org/)
- [Pinia 文档](https://pinia.vuejs.org/zh/)

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
