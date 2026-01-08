# 个人知识管理系统（PKS）- 系统架构设计文档

**文档版本**：v1.0
**创建日期**：2026-01-08
**架构师**：后端系统架构师
**状态**：规划阶段

---

## 1. 技术选型论证

### 1.1 后端技术栈：Python + FastAPI

#### 选择理由

**性能优势：**
- FastAPI 基于 Starlette 和 Pydantic 构建，性能可媲美 Node.js 和 Go
- 原生支持异步编程（async/await），适合高并发场景
- 自动生成 OpenAPI 文档，减少维护成本

**开发效率：**
- 类型提示（Type Hints）减少运行时错误
- 自动数据验证和序列化（Pydantic）
- 依赖注入系统，便于测试和扩展

**生态优势：**
- Python 生态丰富（数据处理、AI集成潜力）
- SQLAlchemy ORM 成熟稳定，支持多数据库
- SQLite → PostgreSQL 迁移成本低

**对比其他方案：**
| 技术栈 | 优势 | 劣势 | 选择结论 |
|--------|------|------|----------|
| **FastAPI** | 高性能、易维护、文档自动生成 | 相对年轻 | ✅ 选择 |
| Flask + Flask-RESTful | 轻量、灵活 | 需手动扩展功能 | ❌ 功能扩展成本高 |
| Django REST Framework | 功能完整 | 性能一般，过度封装 | ❌ 单体应用过重 |
| Go + Gin | 性能最佳 | 开发效率较低，生态较小 | ❌ 团队学习成本高 |

### 1.2 前端技术栈：Vue3

#### 选择理由

**渐进式框架：**
- 组件化开发，易于维护和复用
- Composition API 提供更好的逻辑组织
- 双向绑定减少模板代码

**生态完善：**
- Vue Router（路由管理）
- Pinia（状态管理，Vuex 的继任者）
- Element Plus / Ant Design Vue（UI 组件库）

**学习曲线：**
- 相比 React 更易上手
- 单文件组件（SFC）开发体验好
- 中文文档完善，社区活跃

### 1.3 数据库：SQLite（开发）→ PostgreSQL（生产）

#### 选择理由

**开发阶段 - SQLite：**
- 零配置，开箱即用
- 文件级存储，便于备份和迁移
- 适合单用户或小规模部署
- 支持大部分 SQL 标准

**生产阶段 - PostgreSQL：**
- 成熟的关系型数据库，支持复杂查询
- 全文搜索功能（tsvector）性能优异
- JSON 类型支持灵活的内容存储
- 数据隔离和安全机制完善

**迁移方案：**
- 使用 SQLAlchemy 的数据库抽象层
- 应用相同的 ORM 模型
- 仅修改连接字符串即可切换

---

## 2. 系统架构设计

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                         客户端层（Client Layer）                  │
│                                                                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │  Web Browser│  │   Mobile    │  │  Desktop    │            │
│  │  (Vue3 SPA) │  │   (Future)  │  │  (Future)   │            │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘            │
└─────────┼────────────────┼────────────────┼──────────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │ HTTPS
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                       网关层（Gateway Layer）                     │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │         Nginx / Caddy (反向代理 + 静态文件 + SSL)          │ │
│  └───────────────────────────┬───────────────────────────────┘ │
└──────────────────────────────┼─────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       应用层（Application Layer）                │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                    FastAPI 应用服务器                      │ │
│  │  ┌─────────────┬─────────────┬─────────────┬───────────┐ │ │
│  │  │  认证中间件  │  CORS中间件 │  日志中间件  │ 异常处理  │ │ │
│  │  └─────────────┴─────────────┴─────────────┴───────────┘ │ │
│  └───────────────────────────┬───────────────────────────────┘ │
│                              │                                   │
│  ┌───────────────────────────▼───────────────────────────────┐ │
│  │                     API 路由层（Router Layer）              │ │
│  │  ┌──────────┬──────────┬──────────┬──────────┬─────────┐ │ │
│  │  │ 认证路由  │ 卡片路由  │ 标签路由  │ 搜索路由  │ 看板路由│ │ │
│  │  └──────────┴──────────┴──────────┴──────────┴─────────┘ │ │
│  └───────────────────────────┬───────────────────────────────┘ │
└──────────────────────────────┼─────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      业务逻辑层（Service Layer）                 │
│                                                                 │
│  ┌─────────────┬─────────────┬─────────────┬───────────────┐   │
│  │ AuthService │ CardService │ TagService │ SearchService │   │
│  │  (用户认证)  │  (卡片管理)  │  (标签管理)  │  (搜索服务)   │   │
│  └─────────────┴─────────────┴─────────────┴───────────────┘   │
│                                                                 │
│  ┌─────────────┬─────────────┬─────────────┬───────────────┐   │
│  │LinkService  │ KanbanService│ExportService│BatchService   │   │
│  │ (链接管理)   │  (看板管理)  │  (导出服务)  │  (批量操作)   │   │
│  └─────────────┴─────────────┴─────────────┴───────────────┘   │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      数据访问层（Repository Layer）              │
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │               SQLAlchemy ORM + Session 管理                │ │
│  └───────────────────────────┬───────────────────────────────┘ │
│                              │                                   │
│  ┌───────────────────────────▼───────────────────────────────┐ │
│  │                     Repository 模式                         │ │
│  │  ┌──────────┬──────────┬──────────┬──────────┬─────────┐ │ │
│  │  │ UserRepo │ CardRepo │ TagRepo │ LinkRepo │ KanbanRepo│ │ │
│  │  └──────────┴──────────┴──────────┴──────────┴─────────┘ │ │
│  └───────────────────────────┬───────────────────────────────┘ │
└──────────────────────────────┼─────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                       数据存储层（Data Layer）                   │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │   SQLite     │  │   PostgreSQL │  │    Redis     │        │
│  │  (开发环境)   │  │  (生产环境)   │  │  (可选缓存)   │        │
│  │              │  │              │  │              │        │
│  │ - 用户数据    │  │ - 用户数据    │  │ - 会话缓存   │        │
│  │ - 卡片数据    │  │ - 卡片数据    │  │ - 搜索缓存   │        │
│  │ - 关系数据    │  │ - 全文索引    │  │ - 热点数据   │        │
│  └──────────────┘  └──────────────┘  └──────────────┘        │
└─────────────────────────────────────────────────────────────────┘
```

### 2.2 分层架构设计

采用经典的 **三层架构 + 额外的Repository层**：

#### 2.2.1 Controller 层（路由层）

**职责：**
- 接收和验证 HTTP 请求
- 调用 Service 层处理业务逻辑
- 返回标准化 HTTP 响应
- 处理异常和错误码

**设计原则：**
```python
# 伪代码示例
class CardController:
    def __init__(self, card_service: CardService):
        self.card_service = card_service

    async def create_card(self, request: Request):
        # 1. 验证请求数据
        # 2. 调用 Service 层
        # 3. 返回标准化响应
        pass
```

#### 2.2.2 Service 层（业务逻辑层）

**职责：**
- 实现核心业务逻辑
- 协调多个 Repository 完成复合操作
- 处理事务边界
- 实现缓存策略

**设计原则：**
```python
# 伪代码示例
class CardService:
    def __init__(self, card_repo: CardRepository, link_repo: LinkRepository):
        self.card_repo = card_repo
        self.link_repo = link_repo

    async def create_card_with_links(self, card_data: CardCreate, link_ids: List[int]):
        # 1. 创建卡片
        # 2. 创建双向链接
        # 3. 事务管理
        pass
```

#### 2.2.3 Repository 层（数据访问层）

**职责：**
- 封装数据库操作细节
- 提供 CRUD 基础方法
- 实现复杂查询逻辑
- 管理数据库连接和会话

**设计原则：**
```python
# 伪代码示例
class CardRepository:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def find_by_id(self, card_id: int) -> Optional[Card]:
        # 数据库查询逻辑
        pass

    async def search_fulltext(self, keyword: str) -> List[Card]:
        # 全文搜索实现
        pass
```

### 2.3 目录结构设计

```
pks/
├── backend/                         # 后端项目根目录
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI 应用入口
│   │   ├── config.py                # 配置管理
│   │   │
│   │   ├── api/                     # API 路由层（Controller）
│   │   │   ├── __init__.py
│   │   │   ├── dependencies.py      # 依赖注入
│   │   │   └── v1/                  # API v1 版本
│   │   │       ├── __init__.py
│   │   │       ├── auth.py          # 认证路由
│   │   │       ├── cards.py         # 卡片路由
│   │   │       ├── tags.py          # 标签路由
│   │   │       ├── links.py         # 链接路由
│   │   │       ├── search.py        # 搜索路由
│   │   │       ├── kanban.py        # 看板路由
│   │   │       └── export.py        # 导出路由
│   │   │
│   │   ├── core/                    # 核心功能
│   │   │   ├── __init__.py
│   │   │   ├── security.py          # JWT、密码哈希
│   │   │   ├── deps.py              # 全局依赖（如 get_current_user）
│   │   │   └── exceptions.py        # 自定义异常
│   │   │
│   │   ├── models/                  # SQLAlchemy 数据模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── card.py
│   │   │   ├── tag.py
│   │   │   ├── card_link.py
│   │   │   └── kanban.py
│   │   │
│   │   ├── schemas/                 # Pydantic 请求/响应模型
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── card.py
│   │   │   ├── tag.py
│   │   │   ├── common.py            # 通用响应模型
│   │   │   └── query.py             # 查询参数模型
│   │   │
│   │   ├── services/                # 业务逻辑层（Service）
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── card_service.py
│   │   │   ├── tag_service.py
│   │   │   ├── link_service.py
│   │   │   ├── search_service.py
│   │   │   ├── kanban_service.py
│   │   │   ├── export_service.py
│   │   │   └── batch_service.py
│   │   │
│   │   ├── repositories/            # 数据访问层（Repository）
│   │   │   ├── __init__.py
│   │   │   ├── base.py              # 基础 Repository
│   │   │   ├── user_repo.py
│   │   │   ├── card_repo.py
│   │   │   ├── tag_repo.py
│   │   │   ├── link_repo.py
│   │   │   └── kanban_repo.py
│   │   │
│   │   ├── db/                      # 数据库相关
│   │   │   ├── __init__.py
│   │   │   ├── session.py           # 数据库会话管理
│   │   │   ├── base.py              # Base 声明
│   │   │   └── init_db.py           # 初始化脚本
│   │   │
│   │   ├── utils/                   # 工具函数
│   │   │   ├── __init__.py
│   │   │   ├── logger.py            # 日志配置
│   │   │   ├── validators.py        # 数据验证
│   │   │   └── exporters.py         # 导出工具
│   │   │
│   │   └── middleware/              # 中间件
│   │       ├── __init__.py
│   │       ├── cors.py
│   │       ├── logging.py
│   │       └── auth.py
│   │
│   ├── tests/                       # 测试代码
│   │   ├── __init__.py
│   │   ├── conftest.py              # pytest 配置
│   │   ├── test_api/                # API 测试
│   │   ├── test_services/           # Service 测试
│   │   └── test_repositories/       # Repository 测试
│   │
│   ├── alembic/                     # 数据库迁移
│   │   ├── versions/
│   │   └── env.py
│   │
│   ├── requirements.txt             # Python 依赖
│   ├── pytest.ini                   # pytest 配置
│   ├── .env.example                 # 环境变量示例
│   └── run.py                       # 启动脚本
│
├── frontend/                        # 前端项目根目录
│   ├── src/
│   │   ├── api/                     # API 调用封装
│   │   ├── assets/                  # 静态资源
│   │   ├── components/              # Vue 组件
│   │   ├── router/                  # 路由配置
│   │   ├── stores/                  # Pinia 状态管理
│   │   ├── types/                   # TypeScript 类型
│   │   ├── utils/                   # 工具函数
│   │   ├── views/                   # 页面视图
│   │   ├── App.vue
│   │   └── main.ts
│   ├── package.json
│   └── vite.config.ts
│
├── docs/                            # 文档目录
│   ├── architecture.md              # 本文档
│   ├── data-model.md                # 数据模型设计
│   ├── api-design.md                # API 接口设计
│   └── deployment.md                # 部署指南（待创建）
│
├── scripts/                         # 部署和维护脚本
│   ├── setup.sh                     # 初始化脚本
│   ├── deploy.sh                    # 部署脚本
│   └── backup.sh                    # 备份脚本
│
└── README.md                        # 项目说明
```

### 2.4 部署架构设计

#### 2.4.1 开发环境

```
┌─────────────────────────────────────────┐
│           开发者的本地机器                │
│                                         │
│  ┌─────────────┐      ┌─────────────┐  │
│  │  Vue3 前端   │ ◄──► │  FastAPI    │  │
│  │  (npm run   │      │  (uvicorn)  │  │
│  │   dev)      │      │             │  │
│  └─────────────┘      └──────┬──────┘  │
│                              │         │
│                              ▼         │
│                        ┌─────────────┐ │
│                        │   SQLite    │ │
│                        │  (本地文件)  │ │
│                        └─────────────┘ │
└─────────────────────────────────────────┘
```

**特点：**
- 前端热重载（Vite HMR）
- 后端自动重载（uvicorn --reload）
- SQLite 文件数据库
- 无需额外配置

#### 2.4.2 生产环境（国内服务器部署）

**方案一：单机部署（适合个人使用）**

```
┌─────────────────────────────────────────────────────────┐
│                   Linux 服务器 (Ubuntu/CentOS)           │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │              Nginx / Caddy                         │ │
│  │  - 反向代理到 FastAPI                              │ │
│  │  - 托管 Vue3 静态文件                              │ │
│  │  - SSL/TLS 终结                                    │ │
│  └───────────────────────────────────────────────────┘ │
│                          │                               │
│         ┌────────────────┴────────────────┐             │
│         ▼                                 ▼             │
│  ┌─────────────┐                  ┌─────────────┐       │
│  │  Vue3 静态   │                  │  FastAPI    │       │
│  │  文件构建   │                  │  (Gunicorn  │       │
│  │  (dist/)    │                  │   + Uvicorn)│       │
│  └─────────────┘                  └──────┬──────┘       │
│                                          │               │
│                                          ▼               │
│                                  ┌─────────────┐         │
│                                  │ PostgreSQL  │         │
│                                  │  (数据存储)  │         │
│                                  └─────────────┘         │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  Systemd 服务管理                                   │ │
│  │  - pks-backend.service                             │ │
│  │  - pks-nginx.service                               │ │
│  └───────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**部署流程（国内友好）：**

1. **安装依赖（不使用 Docker）：**
   ```bash
   # Python 3.11+
   sudo apt install python3.11 python3.11-venv

   # Node.js 20+
   curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
   sudo apt install -y nodejs

   # PostgreSQL
   sudo apt install postgresql postgresql-contrib

   # Nginx
   sudo apt install nginx
   ```

2. **后端部署：**
   ```bash
   # 创建虚拟环境
   cd /root/projects/pks/backend
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # 配置环境变量
   cp .env.example .env
   # 编辑 .env 配置数据库连接

   # 初始化数据库
   alembic upgrade head

   # 配置 systemd 服务
   sudo cp scripts/pks-backend.service /etc/systemd/system/
   sudo systemctl enable pks-backend
   sudo systemctl start pks-backend
   ```

3. **前端部署：**
   ```bash
   cd /root/projects/pks/frontend
   npm install
   npm run build

   # 部署到 Nginx
   sudo cp -r dist/* /var/www/pks/
   ```

4. **Nginx 配置：**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       # 前端静态文件
       location / {
           root /var/www/pks;
           try_files $uri $uri/ /index.html;
       }

       # 后端 API 代理
       location /api {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

**方案二：未来扩展 - 微服务架构**

当需要支持多用户、高并发时，可演进为：

```
                    ┌──────────────┐
                    │   CDN / WAF  │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Load Balancer│
                    └──────┬───────┘
                           │
         ┌─────────────────┼─────────────────┐
         ▼                 ▼                 ▼
  ┌────────────┐   ┌────────────┐   ┌────────────┐
  │  App Node  │   │  App Node  │   │  App Node  │
  │ Instance 1 │   │ Instance 2 │   │ Instance 3 │
  └────────────┘   └────────────┘   └────────────┘
         │                 │                 │
         └─────────────────┼─────────────────┘
                           ▼
                  ┌────────────────┐
                  │   PostgreSQL   │
                  │   (Primary)    │
                  └────────────────┘
                           │
                  ┌────────▼────────┐
                  │  PostgreSQL     │
                  │  (Read Replica) │
                  └─────────────────┘
```

---

## 3. 核心技术实现方案

### 3.1 认证与授权

**技术方案：**
- JWT（JSON Web Token）无状态认证
- Access Token 有效期：2小时
- Refresh Token 有效期：30天
- 密码哈希：bcrypt

**流程：**
```
用户登录 → 验证密码 → 生成 JWT Token → 返回给客户端
  │
  ├─ Access Token: 用于 API 请求（放在 Authorization Header）
  └─ Refresh Token: 用于刷新 Access Token（存储在 HttpOnly Cookie）
```

### 3.2 全文搜索实现

**SQLite 方案（开发环境）：**
- 使用 FTS5（Full-Text Search）扩展
- 创建虚拟表：`cards_fts`
- 搜索字段：title, content

**PostgreSQL 方案（生产环境）：**
- 使用内置的全文搜索功能
- 创建 tsvector 类型的字段
- 使用 GIN 索引加速查询
- 支持中文分词（zhparser）

### 3.3 双向链接实现

**技术方案：**
- 卡片关联表（card_links）存储有向关系
- 创建双向关系时，插入两条记录（A→B 和 B→A）
- 查询时自动返回所有关联的卡片

**示例：**
```
卡片A 链接到 卡片B
  ├─ 正向关系：A → B (card_links 表记录)
  └─ 反向关系：B → A (card_links 表记录)
```

### 3.4 性能优化策略

**数据库层：**
- 索引优化：为常用查询字段创建索引
- 查询优化：避免 N+1 查询，使用 eager loading
- 分页：所有列表接口都支持分页

**应用层：**
- 响应压缩：使用 gzip
- 缓存策略：
  - 热点数据缓存（可选 Redis）
  - HTTP 缓存头（ETag、Last-Modified）
  - 静态资源 CDN（未来扩展）

**前端层：**
- 虚拟滚动（长列表）
- 防抖/节流（搜索输入）
- 代码分割（按需加载）

---

## 4. 安全设计

### 4.1 认证安全

- 密码强度校验（最少 8 位，包含字母和数字）
- JWT Token 签名验证
- Refresh Token 存储在 HttpOnly Cookie（防止 XSS）
- 限制登录失败次数（防暴力破解）

### 4.2 API 安全

- 所有 API 需要认证（除登录/注册）
- 用户数据隔离（WHERE user_id = current_user.id）
- CORS 配置（限制允许的域名）
- 请求频率限制（Rate Limiting）

### 4.3 数据安全

- SQL 注入防护（使用 ORM 参数化查询）
- XSS 防护（前端转义，CSP 策略）
- CSRF 防护（SameSite Cookie）
- 敏感数据加密（数据库层面）

### 4.4 日志与审计

- 记录所有敏感操作（创建、删除）
- 记录登录/登出事件
- 错误日志（不记录敏感信息）
- 定期备份（自动脚本）

---

## 5. 可扩展性设计

### 5.1 水平扩展预留

- 无状态 API 设计（Session 存储在 Token 中）
- 数据库连接池管理
- 静态资源可迁移到对象存储（OSS）

### 5.2 功能扩展预留

**多人协作：**
- 数据模型已预留 user_id 字段
- 可添加权限表（permissions）
- 可添加协作表（collaborators）

**版本历史：**
- 可添加 card_versions 表
- 记录每次修改的 diff
- 支持版本回滚

**标签系统：**
- 当前设计支持层级标签
- 可扩展为知识图谱（Graph Database）

---

## 6. 监控与运维

### 6.1 日志系统

**日志级别：**
- DEBUG：开发调试
- INFO：关键操作（登录、CRUD）
- WARNING：异常但可恢复
- ERROR：需要关注的错误

**日志格式：**
```json
{
  "timestamp": "2026-01-08T12:00:00Z",
  "level": "INFO",
  "message": "User logged in",
  "user_id": 123,
  "ip": "192.168.1.1",
  "request_id": "abc123"
}
```

### 6.2 健康检查

**端点：** `GET /api/health`

**响应：**
```json
{
  "status": "healthy",
  "database": "connected",
  "version": "1.0.0"
}
```

### 6.3 备份策略

**数据库备份：**
- 每日自动备份（cron 任务）
- 保留最近 7 天的备份
- 备份文件加密存储

**备份脚本：** `scripts/backup.sh`

---

## 7. 开发规范

### 7.1 代码风格

- Python：遵循 PEP 8
- 使用 Black 自动格式化
- 使用 isort 排序 imports
- 类型提示：所有函数都应有类型注解

### 7.2 Git 工作流

- 主分支：`main`（生产环境）
- 开发分支：`develop`（开发环境）
- 功能分支：`feature/xxx`（新功能）
- 修复分支：`fix/xxx`（Bug 修复）

**提交信息规范：**
```
feat: 添加卡片批量删除功能
fix: 修复搜索结果不准确的bug
docs: 更新 API 文档
refactor: 重构 CardService 代码结构
```

### 7.3 测试策略

**单元测试：**
- 覆盖率目标：> 80%
- 测试 Service 和 Repository 层
- 使用 pytest + pytest-asyncio

**集成测试：**
- 测试 API 端到端流程
- 使用 TestDatabase（SQLite 内存数据库）

---

## 8. 总结

本架构设计遵循以下原则：

✅ **简单性**：避免过度设计，适合单用户或小团队
✅ **可扩展**：预留扩展接口，支持未来功能迭代
✅ **可维护**：清晰的分层架构，易于理解和修改
✅ **高性能**：异步处理 + 索引优化 + 缓存策略
✅ **安全性**：多层安全防护，保障数据安全

**下一步行动：**
1. 搭建基础项目结构
2. 实现数据模型和数据库迁移
3. 实现认证模块
4. 实现卡片 CRUD 功能
5. 实现搜索和双向链接功能

---

**文档维护：** 本文档应随项目演进持续更新
**问题反馈：** 如有疑问或建议，请联系架构师
