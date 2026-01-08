# PKS Backend

个人知识管理系统（Personal Knowledge System）后端服务

## 技术栈

- **框架**: FastAPI 0.109.0
- **ORM**: SQLAlchemy 2.0.25
- **数据库**: SQLite (开发环境) / PostgreSQL (生产环境)
- **迁移**: Alembic 1.13.1
- **认证**: JWT (python-jose)
- **密码哈希**: bcrypt (passlib)

## 项目结构

```
backend/
├── app/
│   ├── api/              # API路由层
│   ├── core/             # 核心配置
│   ├── models/           # SQLAlchemy数据模型
│   ├── schemas/          # Pydantic模式
│   ├── services/         # 业务逻辑层
│   ├── utils/            # 工具函数
│   └── main.py           # FastAPI应用入口
├── alembic/              # 数据库迁移
├── requirements.txt      # Python依赖
└── README.md            # 项目说明
```

## 快速开始

### 1. 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

### 2. 配置环境变量（可选）

创建 `.env` 文件（可使用默认配置）：

```env
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite:///./pks.db
```

### 3. 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head
```

### 4. 启动服务

```bash
# 开发模式（自动重载）
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. 访问API文档

启动服务后，访问以下地址查看自动生成的API文档：

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API端点

### 认证 (`/api/v1/auth`)
- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `GET /me` - 获取当前用户信息

### 卡片 (`/api/v1/cards`)
- `POST /` - 创建卡片
- `GET /` - 获取卡片列表（支持筛选、搜索、分页）
- `GET /{card_id}` - 获取卡片详情
- `PUT /{card_id}` - 更新卡片
- `DELETE /{card_id}` - 删除卡片
- `POST /batch-delete` - 批量删除卡片

### 标签 (`/api/v1/tags`)
- `POST /` - 创建标签
- `GET /` - 获取标签列表（支持层级）
- `GET /{tag_id}` - 获取标签详情
- `PUT /{tag_id}` - 更新标签
- `DELETE /{tag_id}` - 删除标签

### 卡片链接 (`/api/v1/cards`)
- `POST /{card_id}/links` - 创建卡片链接（双向）
- `GET /{card_id}/links` - 获取卡片的所有链接
- `DELETE /{card_id}/links/{target_card_id}` - 删除卡片链接

### 搜索 (`/api/v1/search`)
- `GET /` - 全局搜索（卡片和标签）

### 看板 (`/api/v1/kanban`)
- `GET /` - 获取看板配置
- `POST /columns` - 创建看板列
- `PUT /columns/{column_id}` - 更新看板列
- `DELETE /columns/{column_id}` - 删除看板列
- `POST /cards/move` - 移动卡片
- `POST /cards/batch-move` - 批量移动卡片

## 数据库迁移

### 创建新迁移

```bash
alembic revision --autogenerate -m "描述信息"
```

### 执行迁移

```bash
# 升级到最新版本
alembic upgrade head

# 回退一个版本
alembic downgrade -1

# 查看当前版本
alembic current

# 查看迁移历史
alembic history
```

## 开发指南

### 代码规范

- 使用 Black 自动格式化代码
- 使用 isort 排序 imports
- 遵循 PEP 8 规范

```bash
# 格式化代码
black app/
isort app/
```

### 测试

```bash
# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app --cov-report=html
```

### 数据模型关系

```
User (1) ──< (N) Card
  │                 │
  │                 ├─< (N) CardTag >─ (N) Tag
  │                 │
  │                 ├─< (N) CardLink (source)
  │                 │
  │                 └─ (N) CardLink (target) >─┐
  │                                           │
  └─< (N) Tag                                 │
        │                                     │
        └─ (1) >─< (N) Tag (parent_id, self-referential)
```

## 配置说明

主要配置项（`app/core/config.py`）：

- `SECRET_KEY`: JWT签名密钥（生产环境必须修改）
- `DATABASE_URL`: 数据库连接字符串
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 访问令牌有效期（默认2小时）
- `REFRESH_TOKEN_EXPIRE_DAYS`: 刷新令牌有效期（默认30天）
- `BACKEND_CORS_ORIGINS`: 允许的CORS来源

## 部署建议

### 生产环境配置

1. 使用 PostgreSQL 替代 SQLite
2. 修改 `SECRET_KEY` 为强随机字符串
3. 配置 `BACKEND_CORS_ORIGINS` 为实际域名
4. 使用 Gunicorn + Uvicorn workers
5. 配置 Nginx 作为反向代理

### Docker部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 常见问题

### 1. 数据库连接错误

检查 `DATABASE_URL` 配置是否正确，SQLite 需要绝对路径。

### 2. CORS 错误

在 `BACKEND_CORS_ORIGINS` 中添加前端地址。

### 3. Token 过期

默认访问令牌有效期为2小时，刷新令牌为30天，可在配置中修改。

## 相关文档

- [系统架构设计](../docs/architecture.md)
- [数据模型设计](../docs/data-model.md)
- [API接口设计](../docs/api-design.md)
- [FastAPI 官方文档](https://fastapi.tiangolo.com/)
- [SQLAlchemy 文档](https://docs.sqlalchemy.org/)
