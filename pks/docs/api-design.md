# 个人知识管理系统（PKS）- API 接口设计文档

**文档版本**：v1.0
**创建日期**：2026-01-08
**架构师**：后端系统架构师
**状态**：规划阶段

---

## 1. API 设计概述

### 1.1 设计原则

**RESTful 风格：**
- 使用标准 HTTP 方法（GET、POST、PUT、DELETE）
- 资源导向的 URL 设计
- 统一的响应格式
- 合理的 HTTP 状态码使用

**版本控制：**
- 所有 API 路径前缀：`/api/v1`
- 未来兼容性：通过版本号控制升级

**安全设计：**
- JWT 认证（除注册/登录外，所有 API 需认证）
- 用户数据隔离（所有查询都基于 user_id）
- 请求频率限制（防止滥用）

### 1.2 基础 URL

```
开发环境：http://localhost:8000/api/v1
生产环境：https://your-domain.com/api/v1
```

### 1.3 统一响应格式

**成功响应：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    // 具体数据
  }
}
```

**错误响应：**
```json
{
  "code": 1001,
  "message": "错误描述信息",
  "errors": {
    // 详细错误信息（可选）
    "field": ["错误详情"]
  }
}
```

### 1.4 HTTP 状态码规范

| 状态码 | 说明 | 使用场景 |
|--------|------|---------|
| 200 | OK | 请求成功 |
| 201 | Created | 资源创建成功 |
| 204 | No Content | 删除成功（无返回内容） |
| 400 | Bad Request | 请求参数错误 |
| 401 | Unauthorized | 未认证或 Token 失效 |
| 403 | Forbidden | 无权限访问 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 资源冲突（如重复创建） |
| 422 | Unprocessable Entity | 数据验证失败 |
| 429 | Too Many Requests | 请求频率超限 |
| 500 | Internal Server Error | 服务器内部错误 |

### 1.5 错误码规范

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 1001 | 参数错误 |
| 1002 | 数据验证失败 |
| 1003 | 资源不存在 |
| 1004 | 资源冲突（如重复） |
| 2001 | 未认证 |
| 2002 | Token 过期 |
| 2003 | 无权限 |
| 3001 | 数据库错误 |
| 3002 | 第三方服务错误 |
| 5000 | 服务器内部错误 |

---

## 2. 认证接口

### 2.1 用户注册

**接口地址：** `POST /api/v1/auth/register`

**请求参数：**
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

**请求验证：**
- username：3-50 个字符，只能包含字母、数字、下划线
- email：有效的邮箱格式
- password：最少 8 位，包含字母和数字

**成功响应（201）：**
```json
{
  "code": 0,
  "message": "注册成功",
  "data": {
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com",
      "created_at": "2026-01-08T12:00:00Z"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

**错误响应：**
- 400：参数错误
- 409：用户名或邮箱已存在
- 422：数据验证失败

### 2.2 用户登录

**接口地址：** `POST /api/v1/auth/login`

**请求参数：**
```json
{
  "username": "testuser",
  "password": "password123"
}
```

**或者使用邮箱登录：**
```json
{
  "email": "test@example.com",
  "password": "password123"
}
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "登录成功",
  "data": {
    "user": {
      "id": 1,
      "username": "testuser",
      "email": "test@example.com"
    },
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

**错误响应：**
- 400：参数错误
- 401：用户名或密码错误
- 422：数据验证失败

### 2.3 刷新 Token

**接口地址：** `POST /api/v1/auth/refresh`

**请求头：**
```
Cookie: refresh_token=<refresh_token>
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "刷新成功",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "token_type": "bearer"
  }
}
```

**错误响应：**
- 401：Refresh Token 无效或过期

### 2.4 获取当前用户信息

**接口地址：** `GET /api/v1/auth/me`

**请求头：**
```
Authorization: Bearer <access_token>
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "is_active": true,
    "created_at": "2026-01-08T12:00:00Z"
  }
}
```

**错误响应：**
- 401：未认证

---

## 3. 卡片管理接口

### 3.1 创建卡片

**接口地址：** `POST /api/v1/cards`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "title": "如何学习 FastAPI",
  "content": "FastAPI 是一个现代化的 Python Web 框架...",
  "card_type": "note",
  "url": null,
  "tag_ids": [1, 2],
  "link_ids": [5, 10]
}
```

**字段说明：**
- title：卡片标题（1-200 字符）
- content：卡片内容（根据 card_type 不同，格式不同）
- card_type：卡片类型（note/link/image/code）
- url：网页链接（仅当 type=link 时必填）
- tag_ids：标签 ID 数组（可选）
- link_ids：关联的卡片 ID 数组（可选，创建双向链接）

**成功响应（201）：**
```json
{
  "code": 0,
  "message": "创建成功",
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "如何学习 FastAPI",
    "content": "FastAPI 是一个现代化的 Python Web 框架...",
    "card_type": "note",
    "url": null,
    "is_pinned": false,
    "view_count": 0,
    "tags": [
      {
        "id": 1,
        "name": "编程",
        "color": "#1976D2"
      }
    ],
    "links": [
      {
        "id": 5,
        "title": "Python 异步编程"
      }
    ],
    "created_at": "2026-01-08T12:00:00Z",
    "updated_at": "2026-01-08T12:00:00Z"
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证
- 422：数据验证失败

### 3.2 获取卡片列表

**接口地址：** `GET /api/v1/cards`

**请求头：**
```
Authorization: Bearer <access_token>
```

**查询参数：**
- page：页码（默认 1）
- page_size：每页数量（默认 20，最大 100）
- card_type：卡片类型筛选（可选）
- tag_id：标签筛选（可选）
- is_pinned：是否只显示置顶（可选）
- search：搜索关键词（可选，全文搜索）
- sort_by：排序字段（created_at/updated_at/view_count，默认 created_at）
- order：排序方向（asc/desc，默认 desc）

**示例请求：**
```
GET /api/v1/cards?page=1&page_size=20&card_type=note&tag_id=1&search=FastAPI&sort_by=created_at&order=desc
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "title": "如何学习 FastAPI",
        "content": "FastAPI 是一个现代化的 Python Web 框架...",
        "card_type": "note",
        "url": null,
        "is_pinned": false,
        "view_count": 10,
        "tags": [
          {
            "id": 1,
            "name": "编程",
            "color": "#1976D2"
          }
        ],
        "created_at": "2026-01-08T12:00:00Z",
        "updated_at": "2026-01-08T12:00:00Z"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  }
}
```

**错误响应：**
- 401：未认证

### 3.3 获取卡片详情

**接口地址：** `GET /api/v1/cards/{card_id}`

**请求头：**
```
Authorization: Bearer <access_token>
```

**路径参数：**
- card_id：卡片 ID

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "user_id": 1,
    "title": "如何学习 FastAPI",
    "content": "FastAPI 是一个现代化的 Python Web 框架...",
    "card_type": "note",
    "url": null,
    "is_pinned": false,
    "view_count": 11,
    "tags": [
      {
        "id": 1,
        "name": "编程",
        "color": "#1976D2"
      }
    ],
    "links": {
      "outgoing": [
        {
          "id": 5,
          "title": "Python 异步编程",
          "link_type": "reference"
        }
      ],
      "incoming": [
        {
          "id": 10,
          "title": "Web 框架对比",
          "link_type": "related"
        }
      ]
    },
    "created_at": "2026-01-08T12:00:00Z",
    "updated_at": "2026-01-08T12:00:00Z"
  }
}
```

**错误响应：**
- 401：未认证
- 403：无权访问
- 404：卡片不存在

### 3.4 更新卡片

**接口地址：** `PUT /api/v1/cards/{card_id}`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**路径参数：**
- card_id：卡片 ID

**请求参数：**
```json
{
  "title": "如何学习 FastAPI（更新版）",
  "content": "FastAPI 是一个现代化的 Python Web 框架...",
  "card_type": "note",
  "url": null,
  "is_pinned": true,
  "tag_ids": [1, 2, 3]
}
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "更新成功",
  "data": {
    "id": 1,
    "title": "如何学习 FastAPI（更新版）",
    "content": "FastAPI 是一个现代化的 Python Web 框架...",
    "card_type": "note",
    "url": null,
    "is_pinned": true,
    "view_count": 11,
    "tags": [
      {
        "id": 1,
        "name": "编程",
        "color": "#1976D2"
      }
    ],
    "updated_at": "2026-01-08T13:00:00Z"
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证
- 403：无权访问
- 404：卡片不存在
- 422：数据验证失败

### 3.5 删除卡片

**接口地址：** `DELETE /api/v1/cards/{card_id}`

**请求头：**
```
Authorization: Bearer <access_token>
```

**路径参数：**
- card_id：卡片 ID

**成功响应（204）：**
```
（无内容）
```

**错误响应：**
- 401：未认证
- 403：无权访问
- 404：卡片不存在

### 3.6 批量删除卡片

**接口地址：** `POST /api/v1/cards/batch-delete`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "card_ids": [1, 2, 3, 4, 5]
}
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "删除成功",
  "data": {
    "deleted_count": 5
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证

---

## 4. 标签管理接口

### 4.1 创建标签

**接口地址：** `POST /api/v1/tags`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "name": "编程",
  "color": "#1976D2",
  "parent_id": null
}
```

**字段说明：**
- name：标签名称（1-50 字符）
- color：标签颜色（十六进制，如 #1976D2）
- parent_id：父标签 ID（可选，用于层级标签）

**成功响应（201）：**
```json
{
  "code": 0,
  "message": "创建成功",
  "data": {
    "id": 1,
    "user_id": 1,
    "name": "编程",
    "color": "#1976D2",
    "parent_id": null,
    "created_at": "2026-01-08T12:00:00Z"
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证
- 409：标签名称已存在
- 422：数据验证失败

### 4.2 获取标签列表

**接口地址：** `GET /api/v1/tags`

**请求头：**
```
Authorization: Bearer <access_token>
```

**查询参数：**
- parent_id：父标签 ID（可选，null 表示获取根标签）

**示例请求：**
```
GET /api/v1/tags?parent_id=null
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "name": "编程",
        "color": "#1976D2",
        "parent_id": null,
        "children_count": 2,
        "cards_count": 10,
        "created_at": "2026-01-08T12:00:00Z"
      }
    ],
    "total": 10
  }
}
```

**错误响应：**
- 401：未认证

### 4.3 获取标签详情

**接口地址：** `GET /api/v1/tags/{tag_id}`

**请求头：**
```
Authorization: Bearer <access_token>
```

**路径参数：**
- tag_id：标签 ID

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "id": 1,
    "name": "编程",
    "color": "#1976D2",
    "parent_id": null,
    "children": [
      {
        "id": 2,
        "name": "Python",
        "color": "#1976D2",
        "parent_id": 1
      }
    ],
    "cards": [
      {
        "id": 1,
        "title": "如何学习 FastAPI"
      }
    ],
    "created_at": "2026-01-08T12:00:00Z"
  }
}
```

**错误响应：**
- 401：未认证
- 403：无权访问
- 404：标签不存在

### 4.4 更新标签

**接口地址：** `PUT /api/v1/tags/{tag_id}`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**路径参数：**
- tag_id：标签 ID

**请求参数：**
```json
{
  "name": "编程技术",
  "color": "#FF5733"
}
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "更新成功",
  "data": {
    "id": 1,
    "name": "编程技术",
    "color": "#FF5733",
    "updated_at": "2026-01-08T13:00:00Z"
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证
- 403：无权访问
- 404：标签不存在
- 422：数据验证失败

### 4.5 删除标签

**接口地址：** `DELETE /api/v1/tags/{tag_id}`

**请求头：**
```
Authorization: Bearer <access_token>
```

**路径参数：**
- tag_id：标签 ID

**成功响应（204）：**
```
（无内容）
```

**错误响应：**
- 401：未认证
- 403：无权访问
- 404：标签不存在

### 4.6 批量打标签

**接口地址：** `POST /api/v1/cards/batch-tag`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "card_ids": [1, 2, 3],
  "tag_ids": [5, 10]
}
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "操作成功",
  "data": {
    "affected_count": 3
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证

---

## 5. 双向链接接口

### 5.1 创建卡片链接

**接口地址：** `POST /api/v1/cards/{card_id}/links`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**路径参数：**
- card_id：源卡片 ID

**请求参数：**
```json
{
  "target_card_id": 5,
  "link_type": "reference"
}
```

**字段说明：**
- target_card_id：目标卡片 ID
- link_type：链接类型（reference/related/parent）

**成功响应（201）：**
```json
{
  "code": 0,
  "message": "创建成功",
  "data": {
    "source_card": {
      "id": 1,
      "title": "如何学习 FastAPI"
    },
    "target_card": {
      "id": 5,
      "title": "Python 异步编程"
    },
    "link_type": "reference",
    "created_at": "2026-01-08T12:00:00Z"
  }
}
```

**错误响应：**
- 400：参数错误（如链接到自己）
- 401：未认证
- 404：卡片不存在
- 409：链接已存在

### 5.2 获取卡片的所有链接

**接口地址：** `GET /api/v1/cards/{card_id}/links`

**请求头：**
```
Authorization: Bearer <access_token>
```

**路径参数：**
- card_id：卡片 ID

**查询参数：**
- link_type：链接类型筛选（可选）

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "outgoing": [
      {
        "id": 5,
        "title": "Python 异步编程",
        "link_type": "reference",
        "created_at": "2026-01-08T12:00:00Z"
      }
    ],
    "incoming": [
      {
        "id": 10,
        "title": "Web 框架对比",
        "link_type": "related",
        "created_at": "2026-01-08T11:00:00Z"
      }
    ],
    "total": 2
  }
}
```

**错误响应：**
- 401：未认证
- 404：卡片不存在

### 5.3 删除卡片链接

**接口地址：** `DELETE /api/v1/cards/{card_id}/links/{target_card_id}`

**请求头：**
```
Authorization: Bearer <access_token>
```

**路径参数：**
- card_id：源卡片 ID
- target_card_id：目标卡片 ID

**成功响应（204）：**
```
（无内容）
```

**错误响应：**
- 401：未认证
- 404：链接不存在

---

## 6. 搜索接口

### 6.1 全局搜索

**接口地址：** `GET /api/v1/search`

**请求头：**
```
Authorization: Bearer <access_token>
```

**查询参数：**
- q：搜索关键词（必填）
- type：搜索类型（all/cards/tags，默认 all）
- page：页码（默认 1）
- page_size：每页数量（默认 20）

**示例请求：**
```
GET /api/v1/search?q=FastAPI&type=all&page=1&page_size=20
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "cards": {
      "items": [
        {
          "id": 1,
          "title": "如何学习 FastAPI",
          "content": "FastAPI 是一个现代化的 Python Web 框架...",
          "card_type": "note",
          "highlight": "<em>FastAPI</em> 是一个现代化的 Python Web 框架...",
          "created_at": "2026-01-08T12:00:00Z"
        }
      ],
      "total": 10
    },
    "tags": {
      "items": [
        {
          "id": 1,
          "name": "FastAPI",
          "color": "#1976D2",
          "cards_count": 5
        }
      ],
      "total": 2
    },
    "total": 12
  }
}
```

**错误响应：**
- 400：参数错误（q 为空）
- 401：未认证

### 6.2 高级搜索

**接口地址：** `POST /api/v1/search/advanced`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "keywords": "FastAPI",
  "card_types": ["note", "code"],
  "tag_ids": [1, 2],
  "date_range": {
    "start": "2026-01-01T00:00:00Z",
    "end": "2026-01-08T23:59:59Z"
  },
  "is_pinned": false,
  "page": 1,
  "page_size": 20
}
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [
      {
        "id": 1,
        "title": "如何学习 FastAPI",
        "content": "FastAPI 是一个现代化的 Python Web 框架...",
        "card_type": "note",
        "tags": [
          {
            "id": 1,
            "name": "编程"
          }
        ],
        "created_at": "2026-01-08T12:00:00Z"
      }
    ],
    "total": 5,
    "page": 1,
    "page_size": 20
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证

---

## 7. 看板管理接口

### 7.1 获取看板配置

**接口地址：** `GET /api/v1/kanban`

**请求头：**
```
Authorization: Bearer <access_token>
```

**成功响应（200）：**
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
        "cards": [
          {
            "id": 1,
            "title": "学习 FastAPI",
            "position": 0
          }
        ]
      },
      {
        "id": 2,
        "name": "进行中",
        "position": 1,
        "cards_count": 3,
        "cards": [
          {
            "id": 5,
            "title": "实现卡片 CRUD",
            "position": 0
          }
        ]
      },
      {
        "id": 3,
        "name": "已完成",
        "position": 2,
        "cards_count": 10,
        "cards": []
      }
    ]
  }
}
```

**错误响应：**
- 401：未认证

### 7.2 创建看板列

**接口地址：** `POST /api/v1/kanban/columns`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "name": "测试中",
  "position": 3
}
```

**成功响应（201）：**
```json
{
  "code": 0,
  "message": "创建成功",
  "data": {
    "id": 4,
    "name": "测试中",
    "position": 3,
    "created_at": "2026-01-08T12:00:00Z"
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证
- 409：位置冲突

### 7.3 更新看板列

**接口地址：** `PUT /api/v1/kanban/columns/{column_id}`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**路径参数：**
- column_id：列 ID

**请求参数：**
```json
{
  "name": "已归档",
  "position": 4
}
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "更新成功",
  "data": {
    "id": 4,
    "name": "已归档",
    "position": 4,
    "updated_at": "2026-01-08T13:00:00Z"
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证
- 403：无权访问
- 404：列不存在

### 7.4 删除看板列

**接口地址：** `DELETE /api/v1/kanban/columns/{column_id}`

**请求头：**
```
Authorization: Bearer <access_token>
```

**路径参数：**
- column_id：列 ID

**成功响应（204）：**
```
（无内容）
```

**错误响应：**
- 401：未认证
- 403：无权访问
- 404：列不存在

### 7.5 移动卡片到看板列

**接口地址：** `POST /api/v1/kanban/cards/move`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "card_id": 1,
  "column_id": 2,
  "position": 0
}
```

**字段说明：**
- card_id：卡片 ID
- column_id：目标列 ID
- position：在列中的位置

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "移动成功",
  "data": {
    "card_id": 1,
    "column_id": 2,
    "position": 0
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证
- 404：卡片或列不存在

### 7.6 批量移动卡片

**接口地址：** `POST /api/v1/kanban/cards/batch-move`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "card_ids": [1, 2, 3],
  "target_column_id": 2
}
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "移动成功",
  "data": {
    "moved_count": 3
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证

---

## 8. 数据导出接口

### 8.1 导出为 JSON

**接口地址：** `POST /api/v1/export/json`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "card_ids": [1, 2, 3],
  "include_links": true,
  "include_tags": true
}
```

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "导出成功",
  "data": {
    "export_url": "https://your-domain.com/exports/2026-01-08_cards_export.json",
    "cards_count": 3,
    "file_size": 1024,
    "expires_at": "2026-01-09T12:00:00Z"
  }
}
```

**或者直接返回文件（Content-Type: application/json）：**
```json
[
  {
    "id": 1,
    "title": "如何学习 FastAPI",
    "content": "FastAPI 是一个现代化的 Python Web 框架...",
    "card_type": "note",
    "tags": ["编程", "Python"],
    "links": [5, 10],
    "created_at": "2026-01-08T12:00:00Z"
  }
]
```

**错误响应：**
- 400：参数错误
- 401：未认证

### 8.2 导出为 Markdown

**接口地址：** `POST /api/v1/export/markdown`

**请求头：**
```
Authorization: Bearer <access_token>
Content-Type: application/json
```

**请求参数：**
```json
{
  "card_ids": [1, 2, 3],
  "include_tags": true,
  "include_links": true
}
```

**成功响应（200）：**
```
Content-Type: text/markdown
Content-Disposition: attachment; filename="cards_export.md"

# 如何学习 FastAPI

**标签：** 编程, Python
**创建时间：** 2026-01-08

FastAPI 是一个现代化的 Python Web 框架...

---

# Python 异步编程

**标签：** 编程
**创建时间：** 2026-01-07

Python 的 asyncio 库提供了强大的异步编程能力...
```

**错误响应：**
- 400：参数错误
- 401：未认证

### 8.3 导出所有数据

**接口地址：** `POST /api/v1/export/all`

**请求头：**
```
Authorization: Bearer <access_token>
```

**请求参数：**
```json
{
  "format": "json"
}
```

**format 支持：**
- json：导出为 JSON 格式
- markdown：导出为 Markdown 格式
- csv：导出为 CSV 格式（仅卡片）

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "导出成功",
  "data": {
    "export_url": "https://your-domain.com/exports/2026-01-08_full_backup.json",
    "file_size": 5120,
    "expires_at": "2026-01-09T12:00:00Z"
  }
}
```

**错误响应：**
- 400：参数错误
- 401：未认证

---

## 9. 统计与分析接口

### 9.1 获取统计数据

**接口地址：** `GET /api/v1/stats`

**请求头：**
```
Authorization: Bearer <access_token>
```

**查询参数：**
- period：统计周期（all/week/month/year，默认 all）

**成功响应（200）：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "cards": {
      "total": 100,
      "by_type": {
        "note": 50,
        "link": 20,
        "image": 15,
        "code": 15
      },
      "created_this_week": 10,
      "created_this_month": 30
    },
    "tags": {
      "total": 20,
      "most_used": [
        {
          "id": 1,
          "name": "编程",
          "cards_count": 30
        }
      ]
    },
    "links": {
      "total": 50
    },
    "activity": {
      "most_viewed": [
        {
          "id": 1,
          "title": "如何学习 FastAPI",
          "view_count": 100
        }
      ],
      "recently_created": [
        {
          "id": 5,
          "title": "Vue3 组合式 API",
          "created_at": "2026-01-08T12:00:00Z"
        }
      ]
    }
  }
}
```

**错误响应：**
- 401：未认证

---

## 10. 健康检查与系统接口

### 10.1 健康检查

**接口地址：** `GET /api/health`

**说明：** 无需认证

**成功响应（200）：**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2026-01-08T12:00:00Z",
  "database": {
    "status": "connected",
    "latency_ms": 5
  }
}
```

### 10.2 API 版本信息

**接口地址：** `GET /api/v1`

**说明：** 无需认证

**成功响应（200）：**
```json
{
  "name": "PKS API",
  "version": "1.0.0",
  "description": "个人知识管理系统 API",
  "documentation": "https://your-domain.com/docs"
}
```

---

## 11. 错误处理规范

### 11.1 统一错误响应格式

```json
{
  "code": 1001,
  "message": "参数错误",
  "errors": {
    "title": ["标题不能为空"],
    "content": ["内容长度不能超过 10000 个字符"]
  },
  "timestamp": "2026-01-08T12:00:00Z",
  "path": "/api/v1/cards"
}
```

### 11.2 常见错误场景

**参数验证失败（422）：**
```json
{
  "code": 1002,
  "message": "数据验证失败",
  "errors": {
    "username": ["用户名长度必须在 3-50 个字符之间"],
    "email": ["邮箱格式不正确"]
  }
}
```

**未认证（401）：**
```json
{
  "code": 2001,
  "message": "未认证",
  "errors": {
    "detail": "Token 已过期，请重新登录"
  }
}
```

**资源不存在（404）：**
```json
{
  "code": 1003,
  "message": "资源不存在",
  "errors": {
    "detail": "卡片 ID 123 不存在"
  }
}
```

**服务器错误（500）：**
```json
{
  "code": 5000,
  "message": "服务器内部错误",
  "errors": {
    "detail": "请联系管理员"
  }
}
```

---

## 12. API 使用示例

### 12.1 完整的卡片创建流程

```bash
# 1. 注册/登录获取 Token
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'

# 响应：获得 access_token
export TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

# 2. 创建标签
curl -X POST http://localhost:8000/api/v1/tags \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "编程", "color": "#1976D2"}'

# 响应：获得 tag_id = 1

# 3. 创建卡片
curl -X POST http://localhost:8000/api/v1/cards \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "如何学习 FastAPI",
    "content": "FastAPI 是一个现代化的 Python Web 框架...",
    "card_type": "note",
    "tag_ids": [1]
  }'

# 响应：创建成功，card_id = 1

# 4. 创建双向链接
curl -X POST http://localhost:8000/api/v1/cards/1/links \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"target_card_id": 5, "link_type": "reference"}'

# 响应：链接创建成功
```

### 12.2 搜索与导出流程

```bash
# 1. 全局搜索
curl -X GET "http://localhost:8000/api/v1/search?q=FastAPI&type=all" \
  -H "Authorization: Bearer $TOKEN"

# 2. 导出搜索结果为 JSON
curl -X POST http://localhost:8000/api/v1/export/json \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "card_ids": [1, 5, 10],
    "include_links": true,
    "include_tags": true
  }'

# 响应：获得导出文件 URL
```

---

## 13. 性能与限流

### 13.1 请求频率限制

**限制规则：**
- 未认证用户：60 次/分钟
- 已认证用户：300 次/分钟
- 搜索接口：30 次/分钟

**超出限制响应（429）：**
```json
{
  "code": 429,
  "message": "请求频率超限",
  "errors": {
    "retry_after": 30
  }
}
```

### 13.2 分页限制

**默认分页：**
- page_size 默认：20
- page_size 最大：100
- 建议：使用合理的分页大小，避免大量数据传输

---

## 14. 总结

### 14.1 API 设计特点

✅ **RESTful 风格**：标准的 HTTP 方法和状态码
✅ **统一响应格式**：便于前端处理
✅ **完善的错误处理**：清晰的错误码和错误信息
✅ **安全设计**：JWT 认证 + 用户数据隔离
✅ **性能优化**：分页、限流、索引优化
✅ **易于扩展**：版本控制 + 清晰的模块划分

### 14.2 下一步行动

1. 实现 FastAPI 项目基础结构
2. 实现认证模块（JWT）
3. 实现卡片 CRUD 接口
4. 实现搜索和标签接口
5. 编写 API 测试用例
6. 生成 OpenAPI 文档

### 14.3 相关文档

- `architecture.md`：系统架构设计
- `data-model.md`：数据模型设计
- OpenAPI 文档：启动后自动生成（`http://localhost:8000/docs`）

---

**文档维护：** 本文档应随 API 变更同步更新
**问题反馈：** 如有疑问或建议，请联系架构师
