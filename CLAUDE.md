# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**PKS (Personal Knowledge System)** 是一个个人知识管理系统，采用前后端分离架构。该项目是作为 AI 多角色协作（架构师、前端、后端）的测试项目而创建。

- **后端**: FastAPI + SQLAlchemy + Alembic
- **前端**: Vue 3 + Vite + Pinia + Element Plus
- **数据库**: SQLite（开发环境）/ PostgreSQL（生产环境）

项目核心功能包括知识卡片管理、双向链接、全局搜索、看板视图和标签系统。

---

## 开发命令

### 后端 (FastAPI)

```bash
cd pks/backend

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
alembic upgrade head

# 开发模式（自动重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 运行测试
pytest

# 代码格式化
black app/
isort app/

# 创建数据库迁移
alembic revision --autogenerate -m "描述信息"
```

### 前端 (Vue 3)

```bash
cd pks/frontend

# 安装依赖
npm install

# 开发模式
npm run dev

# 生产构建
npm run build

# 预览构建
npm run preview

# 代码检查
npm run lint
```

### API 文档

后端启动后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## 项目架构

### 后端分层架构

```
pks/backend/app/
├── api/v1/          # API 路由层 (Controller) - 处理 HTTP 请求
├── core/            # 核心配置 - JWT、配置文件、依赖注入
├── models/          # SQLAlchemy 数据模型
├── schemas/         # Pydantic 请求/响应模型
├── services/        # 业务逻辑层 - 复杂业务规则
├── db/              # 数据库会话和 Base 类
└── main.py          # FastAPI 应用入口
```

**重要**: 所有数据查询必须包含 `user_id` 过滤以确保数据隔离。

### 前端结构

```
pks/frontend/src/
├── api/             # API 调用封装 - 自动处理 Token 和错误
├── components/      # Vue 组件
├── views/           # 页面视图
├── stores/          # Pinia 状态管理
├── router/          # Vue Router 配置
├── composables/     # Composition API 复用逻辑
└── utils/           # 工具函数
```

### 数据模型关系

```
User (1) ──< (N) Card
  │                 │
  │                 ├─< (N) CardTag >─ (N) Tag
  │                 │
  │                 ├─< (N) CardLink (双向链接)
  │                 │
  │                 └─< (N) KanbanCard >─ (N) KanbanColumn
  │
  └─< (N) Tag (支持层级，parent_id 自引用)
```

**双向链接实现**: 创建卡片 A 到 B 的链接时，需要插入两条记录（A→B 和 B→A）。

---

## 核心概念

### 卡片类型

- `note`: 笔记（Markdown 文本）
- `link`: 网页链接
- `image`: 图片（Base64 或 URL）
- `code`: 代码片段

### 链接类型

- `reference`: 普通引用
- `related`: 相关推荐
- `parent`: 父子关系

### 数据隔离

所有表（除关联表外）都包含 `user_id` 字段。所有查询必须过滤当前用户数据。

### 看板系统

默认 3 列：待处理(0)、进行中(1)、已完成(2)。拖拽操作需要更新 `position` 字段。

---

## 环境配置

### 后端 (.env)

```env
DATABASE_URL=sqlite:///./pks.db
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

### 前端 (.env)

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_TITLE=个人知识管理系统
```

---

## API 端点概览

- `POST /api/v1/auth/register` - 用户注册
- `POST /api/v1/auth/login` - 用户登录
- `GET /api/v1/cards` - 获取卡片列表（支持筛选、搜索、分页）
- `POST /api/v1/cards` - 创建卡片
- `GET /api/v1/cards/{id}` - 获取卡片详情
- `PUT /api/v1/cards/{id}` - 更新卡片
- `DELETE /api/v1/cards/{id}` - 删除卡片
- `POST /api/v1/cards/{id}/links` - 创建卡片链接
- `GET /api/v1/tags` - 获取标签列表
- `GET /api/v1/search` - 全局搜索
- `GET /api/v1/kanban` - 获取看板配置

完整 API 文档见后端 `/docs`。

---

## 相关文档

- 系统架构: `pks/docs/architecture.md`
- 数据模型: `pks/docs/data-model.md`
- API 设计: `pks/docs/api-design.md`
- 部署指南: `pks/docs/deployment.md`
