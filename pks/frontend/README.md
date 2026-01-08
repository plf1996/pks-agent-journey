# PKS Frontend

个人知识管理系统 (Personal Knowledge System) - Vue3 前端应用

## 项目概述

PKS 是一个帮助用户管理和组织碎片化信息的知识管理系统。前端基于 Vue 3 + Vite + Element Plus 构建。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **构建工具**: Vite
- **状态管理**: Pinia
- **路由**: Vue Router
- **UI组件**: Element Plus
- **HTTP客户端**: Axios
- **拖拽**: Vue Draggable Plus

## 功能特性

### 核心功能
- ✅ 用户认证（登录/注册）
- ✅ 卡片管理（CRUD）
- ✅ 标签管理
- ✅ 双向链接
- ✅ 全局搜索
- ✅ 看板视图（拖拽管理）

### 卡片类型
- 📝 笔记
- 🔗 网页链接
- 🖼️ 图片
- 💻 代码片段

## 项目结构

```
frontend/
├── public/                 # 静态资源
├── src/
│   ├── api/                # API调用封装
│   │   ├── index.js        # Axios配置
│   │   ├── auth.js         # 认证API
│   │   ├── cards.js        # 卡片API
│   │   ├── tags.js         # 标签API
│   │   ├── links.js        # 链接API
│   │   ├── search.js       # 搜索API
│   │   └── kanban.js       # 看板API
│   ├── assets/             # 静态资源
│   │   └── styles/         # 全局样式
│   ├── components/         # 组件
│   │   ├── common/         # 通用组件
│   │   ├── cards/          # 卡片组件
│   │   ├── tags/           # 标签组件
│   │   ├── search/         # 搜索组件
│   │   └── kanban/         # 看板组件
│   ├── views/              # 页面视图
│   ├── router/             # 路由配置
│   ├── stores/             # Pinia状态管理
│   ├── composables/        # 组合式函数
│   ├── utils/              # 工具函数
│   ├── App.vue             # 根组件
│   └── main.js             # 入口文件
├── index.html              # HTML模板
├── package.json            # 项目配置
├── vite.config.js          # Vite配置
└── .env.example            # 环境变量示例
```

## 快速开始

### 环境要求

- Node.js >= 16.x
- npm >= 8.x 或 pnpm >= 7.x

### 安装依赖

```bash
cd frontend
npm install
```

### 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=个人知识管理系统
```

### 开发模式

```bash
npm run dev
```

访问 http://localhost:5173

### 生产构建

```bash
npm run build
```

构建产物在 `dist/` 目录

### 预览构建

```bash
npm run preview
```

## API 配置

默认 API 地址为 `http://localhost:8000/api/v1`，可在 `.env` 文件中修改。

### API 响应格式

**成功响应：**
```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

**错误响应：**
```json
{
  "code": 1001,
  "message": "错误描述",
  "errors": {}
}
```

## 状态管理

使用 Pinia 进行状态管理，主要的 Store 包括：

- `authStore`: 用户认证状态
- `cardsStore`: 卡片数据状态
- `tagsStore`: 标签数据状态

## 路由说明

- `/login`: 登录页
- `/register`: 注册页
- `/`: 仪表盘首页
- `/cards`: 卡片列表
- `/cards/:id`: 卡片详情
- `/cards/new`: 新建卡片
- `/cards/:id/edit`: 编辑卡片
- `/tags`: 标签管理
- `/kanban`: 看板视图
- `/search`: 全局搜索
- `/settings`: 设置页面

## 浏览器支持

- Chrome >= 90
- Firefox >= 88
- Safari >= 14
- Edge >= 90

## 开发说明

### 代码规范

- 使用 Composition API
- 使用 `<script setup>` 语法糖
- 组件命名采用 PascalCase
- 文件命名采用 PascalCase (组件) 或 kebab-case (工具函数)

### 样式规范

- 使用 scoped 样式
- 遵循 BEM 命名规范
- 使用 CSS 变量定义主题颜色

### API 调用

所有 API 调用都通过 `src/api/` 目录下的封装函数进行，自动处理：
- 请求拦截（添加 Token）
- 响应拦截（统一错误处理）
- Token 过期自动跳转登录

## 部署

### Nginx 配置示例

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # 前端静态文件
    location / {
        root /var/www/pks/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端 API 代理
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 常见问题

### 1. 跨域问题

开发环境下 Vite 已配置代理，生产环境建议使用 Nginx 反向代理。

### 2. Token 过期

Token 有效期为 2 小时，过期后会自动跳转到登录页。

### 3. 图片上传

当前版本图片类型卡片支持 Base64 编码，生产环境建议使用对象存储。

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请提交 Issue。
