# PKS Backend API 快速参考

## 基础信息

- **Base URL**: `http://localhost:8000`
- **API Version**: `/api/v1`
- **认证方式**: JWT Bearer Token
- **响应格式**: JSON

## 统一响应格式

### 成功响应
```json
{
  "code": 0,
  "message": "success",
  "data": { /* 具体数据 */ }
}
```

### 错误响应
```json
{
  "code": 1001,
  "message": "错误描述",
  "errors": { /* 详细错误 */ }
}
```

## 认证流程

### 1. 注册
```bash
POST /api/v1/auth/register
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

### 2. 登录
```bash
POST /api/v1/auth/login
Content-Type: application/json

{
  "username": "testuser",
  "password": "password123"
}

# 或使用邮箱登录
{
  "email": "test@example.com",
  "password": "password123"
}
```

**响应**:
```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "access_token": "eyJhbG...",
    "refresh_token": "eyJhbG...",
    "token_type": "bearer"
  }
}
```

### 3. 使用Token
```bash
Authorization: Bearer <access_token>
```

## 核心API端点

### 卡片管理

#### 创建卡片
```bash
POST /api/v1/cards
Authorization: Bearer <token>

{
  "title": "如何学习 FastAPI",
  "content": "FastAPI 是一个现代化的 Python Web 框架...",
  "card_type": "note",
  "url": null,
  "tag_ids": [1, 2],
  "link_ids": [5, 10]
}
```

#### 获取卡片列表
```bash
GET /api/v1/cards?page=1&page_size=20&card_type=note&tag_id=1&search=FastAPI&sort_by=created_at&order=desc
Authorization: Bearer <token>
```

#### 获取卡片详情
```bash
GET /api/v1/cards/{card_id}
Authorization: Bearer <token>
```

#### 更新卡片
```bash
PUT /api/v1/cards/{card_id}
Authorization: Bearer <token>

{
  "title": "更新后的标题",
  "content": "更新后的内容",
  "is_pinned": true,
  "tag_ids": [1, 2, 3]
}
```

#### 删除卡片
```bash
DELETE /api/v1/cards/{card_id}
Authorization: Bearer <token>
```

#### 批量删除
```bash
POST /api/v1/cards/batch-delete
Authorization: Bearer <token>

{
  "card_ids": [1, 2, 3, 4, 5]
}
```

### 标签管理

#### 创建标签
```bash
POST /api/v1/tags
Authorization: Bearer <token>

{
  "name": "编程",
  "color": "#1976D2",
  "parent_id": null
}
```

#### 获取标签列表
```bash
GET /api/v1/tags?parent_id=null
Authorization: Bearer <token>
```

#### 获取标签详情
```bash
GET /api/v1/tags/{tag_id}
Authorization: Bearer <token>
```

#### 更新标签
```bash
PUT /api/v1/tags/{tag_id}
Authorization: Bearer <token>

{
  "name": "编程技术",
  "color": "#FF5733"
}
```

#### 删除标签
```bash
DELETE /api/v1/tags/{tag_id}
Authorization: Bearer <token>
```

### 卡片链接

#### 创建链接（双向）
```bash
POST /api/v1/cards/{card_id}/links
Authorization: Bearer <token>

{
  "target_card_id": 5,
  "link_type": "reference"
}
```

**链接类型**:
- `reference`: 普通引用
- `related`: 相关推荐
- `parent`: 父子关系

#### 获取卡片的所有链接
```bash
GET /api/v1/cards/{card_id}/links?link_type=reference
Authorization: Bearer <token>
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "outgoing": [ /* 我链接到的卡片 */ ],
    "incoming": [ /* 链接到我的卡片 */ ],
    "total": 10
  }
}
```

#### 删除链接
```bash
DELETE /api/v1/cards/{card_id}/links/{target_card_id}
Authorization: Bearer <token>
```

### 搜索

#### 全局搜索
```bash
GET /api/v1/search?q=FastAPI&type=all&page=1&page_size=20
Authorization: Bearer <token>
```

**参数**:
- `q`: 搜索关键词（必填）
- `type`: 搜索类型（all/cards/tags）
- `page`: 页码（默认1）
- `page_size`: 每页数量（默认20，最大100）

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "cards": {
      "items": [ /* 卡片列表 */ ],
      "total": 10
    },
    "tags": {
      "items": [ /* 标签列表 */ ],
      "total": 2
    },
    "total": 12
  }
}
```

### 看板管理

#### 获取看板配置
```bash
GET /api/v1/kanban
Authorization: Bearer <token>
```

**响应**:
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "columns": [
      {
        "id": 1,
        "name": "待处理",
        "position": 0,
        "cards_count": 5,
        "cards": [ /* 列中的卡片 */ ]
      }
    ]
  }
}
```

#### 创建看板列
```bash
POST /api/v1/kanban/columns
Authorization: Bearer <token>

{
  "name": "测试中",
  "position": 3
}
```

#### 更新看板列
```bash
PUT /api/v1/kanban/columns/{column_id}
Authorization: Bearer <token>

{
  "name": "已归档",
  "position": 4
}
```

#### 删除看板列
```bash
DELETE /api/v1/kanban/columns/{column_id}
Authorization: Bearer <token>
```

#### 移动卡片
```bash
POST /api/v1/kanban/cards/move
Authorization: Bearer <token>

{
  "card_id": 1,
  "column_id": 2,
  "position": 0
}
```

#### 批量移动卡片
```bash
POST /api/v1/kanban/cards/batch-move
Authorization: Bearer <token>

{
  "card_ids": [1, 2, 3],
  "target_column_id": 2
}
```

## 卡片类型

- `note`: 笔记（Markdown文本）
- `link`: 网页链接（需提供url字段）
- `image`: 图片（Base64或URL）
- `code`: 代码片段

## 分页参数

- `page`: 页码（从1开始）
- `page_size`: 每页数量（默认20，最大100）

## 排序参数

- `sort_by`: 排序字段（created_at/updated_at/view_count）
- `order`: 排序方向（asc/desc）

## 常见错误码

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | 数据验证失败 |
| 1003 | 资源不存在 |
| 1004 | 资源冲突 |
| 2001 | 未认证 |
| 2002 | Token过期 |
| 2003 | 无权限 |
| 5000 | 服务器内部错误 |

## 快速测试

### 使用curl
```bash
# 1. 注册
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}'

# 2. 登录
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# 保存Token
export TOKEN="从登录响应中获取的access_token"

# 3. 创建标签
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"编程","color":"#1976D2"}'

# 4. 创建卡片
curl -X POST http://localhost:8000/api/v1/cards \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"FastAPI学习","content":"FastAPI是一个现代化的框架","card_type":"note","tag_ids":[1]}'

# 5. 搜索
curl -X GET "http://localhost:8000/api/v1/search?q=FastAPI" \
  -H "Authorization: Bearer $TOKEN"
```

### 使用Swagger UI
访问 http://localhost:8000/docs 进行交互式API测试

## 开发提示

1. **首次启动**: 运行 `./run.sh` 自动安装依赖和初始化数据库
2. **查看日志**: 控制台会显示所有请求日志
3. **自动重载**: 开发模式下代码修改会自动重启服务
4. **API文档**: 启动后访问 `/docs` 或 `/redoc`
