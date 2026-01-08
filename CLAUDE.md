# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

**PKS Agent Journey** 是一个实验性探索项目，记录了使用 Claude Code 的多角色 AI Agent 协同开发全栈应用的完整过程。

- **主项目**: PKS (Personal Knowledge System) - 个人知识管理系统
- **目标**: 探索和验证 LLM 在复杂项目开发中的协同模式与边界
- **核心价值**: 完整记录了架构师、前端、后端多 Agent 协同的对话日志、Prompt 设计和决策过程

项目包含两部分：
1. **pks/** - 完整的全栈应用代码
2. **claude-code/** - Agent 角色定义和技能配置

---

## PKS 应用开发命令

### 后端 (FastAPI)

```bash
cd pks/backend

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 设置数据库和密钥配置

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

### Docker 开发环境

```bash
cd pks

# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 初始化数据库
docker-compose -f docker-compose.dev.yml exec backend python scripts/init_db.py

# 停止环境
docker-compose -f docker-compose.dev.yml down
```

### API 文档

后端启动后访问:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

---

## PKS 应用架构

### 后端分层架构

```
pks/backend/app/
├── api/v1/          # API 路由层 (Controller) - 处理 HTTP 请求
│   ├── auth.py       # JWT 认证（注册、登录、Token 刷新）
│   ├── cards.py      # 卡片 CRUD、批量操作、导出
│   ├── tags.py       # 标签管理、层级查询
│   ├── links.py      # 双向链接创建、查询
│   ├── search.py     # 全局搜索（标题、内容、标签）
│   └── kanban.py     # 看板配置、拖拽更新
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
├── components/      # Vue 组件（可复用组件）
├── views/           # 页面视图（路由级组件）
│   ├── Dashboard.vue    # 仪表盘（统计卡片、标签分布）
│   ├── Cards.vue        # 卡片列表（筛选、搜索、分页）
│   ├── CardEditor.vue   # 卡片编辑器（创建/编辑）
│   ├── CardDetail.vue   # 卡片详情（显示、链接管理）
│   ├── Kanban.vue       # 看板视图（拖拽管理）
│   ├── Search.vue       # 搜索页面（全文搜索）
│   ├── Tags.vue         # 标签管理
│   ├── Login.vue        # 登录页面
│   ├── Register.vue     # 注册页面
│   └── Settings.vue     # 用户设置
├── stores/          # Pinia 状态管理
│   ├── auth.js      # 认证状态（Token、用户信息）
│   └── cards.js     # 卡片数据缓存
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

## PKS 核心概念

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

## PKS 环境配置

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

## PKS API 端点概览

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

## Agent 协作配置

### 可用 Agent

项目定义了以下专业化 Agent，通过 `/agent <name>` 或 Task 工具调用：

1. **software-architect** (Opus, 蓝色)
   - 用途: 系统设计、架构规划、技术选型
   - 示例: "设计高可用电商平台的架构"

2. **backend-system-architect** (Sonnet, 绿色)
   - 用途: 后端开发、API 设计、数据库优化、性能调优
   - 示例: "设计每秒处理 1000 订单的系统"

3. **frontend-dev-expert** (Sonnet, 粉色)
   - 用途: 前端开发、组件设计、状态管理、性能优化
   - 示例: "实现带验证的注册表单"

4. **project-manager** (Sonnet, 橙色)
   - 用途: 项目协调、任务分配、进度跟踪、跨角色协作
   - 示例: "启动电商平台项目，协调前后端开发"

### Agent 协作流程示例

```bash
# 1. 项目启动 - 架构师设计
/agent software-architect
> 我需要设计一个知识管理系统，请规划技术架构

# 2. 后端开发
/agent backend-system-architect
> 实现卡片的 CRUD API

# 3. 前端开发
/agent frontend-dev-expert
> 实现卡片列表页面，支持筛选和分页

# 4. 项目协调
/agent project-manager
> 评估整体进度并分配下一步任务
```

### Agent 定义位置

Agent 配置文件位于 `claude-code/agents/`:
- `software-architect.md` - 架构师 Prompt
- `backend-system-architect.md` - 后端专家 Prompt
- `frontend-dev-expert.md` - 前端专家 Prompt
- `project-manager.md` - 项目经理 Prompt

---

## 相关文档

### PKS 应用文档
- 系统架构: `pks/docs/architecture.md`
- 数据模型: `pks/docs/data-model.md`
- API 设计: `pks/docs/api-design.md`
- 部署指南: `pks/docs/deployment.md`

### 项目元文档
- 项目需求: `Project Requirements.md`
- 项目总览: `README.md`
- PKS 应用说明: `pks/README.md`

---

## 开发注意事项

### 当前状态
- PKS 应用代码已完整实现
- 后端 Dockerfile 已配置阿里云镜像源（国内加速）
- 项目处于可运行状态，支持 Docker 和本地开发

### 常见任务
- **修改后端 API**: 编辑 `pks/backend/app/api/v1/` 对应模块
- **添加前端页面**: 在 `pks/frontend/src/views/` 创建组件并配置路由
- **数据库变更**: 使用 Alembic 创建迁移 `alembic revision --autogenerate`
- **调整 Agent 行为**: 编辑 `claude-code/agents/` 对应的 `.md` 文件

### 调试技巧
- 后端日志: 控制台直接输出，查看 API 请求和错误
- 前端调试: 浏览器开发者工具，Vue DevTools 扩展
- API 测试: 使用 Swagger UI (`/docs`) 进行交互式测试
