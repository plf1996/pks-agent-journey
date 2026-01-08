# PKS - 个人知识管理系统

<div align="center">

![PKS Logo](docs/logo.png)

一个轻量级的个人知识管理系统，帮助你收集、整理和关联碎片化知识。

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)](https://fastapi.tiangolo.com)
[![Vue 3](https://img.shields.io/badge/Vue-3.4.0-brightgreen.svg)](https://vuejs.org)

[功能特性](#功能特性) • [快速开始](#快速开始) • [部署指南](#部署指南) • [贡献指南](#贡献指南)

</div>

---

## ✨ 简介

**PKS (Personal Knowledge System)** 是一个全栈个人知识管理系统，让你像管理图书馆一样管理自己的知识库。

- 📝 **知识卡片**：支持笔记、链接、图片、代码四种类型
- 🔗 **双向链接**：建立知识之间的关联，形成知识网络
- 🔍 **全局搜索**：快速找到你需要的内容
- 📋 **看板管理**：可视化整理你的知识
- 🏷️ **标签系统**：灵活分类和筛选

---

## 🎯 功能特性

### 核心功能

| 功能 | 描述 |
|------|------|
| **知识卡片** | 支持笔记、网页链接、图片、代码四种内容类型 |
| **双向链接** | 卡片间可建立关联，自动维护双向关系 |
| **全局搜索** | 按标题、内容、标签进行全文搜索 |
| **看板视图** | 类似 Trello 的拖拽式分类管理 |
| **标签系统** | 支持层级结构的标签分类 |
| **批量操作** | 批量删除、移动、打标签 |
| **数据导出** | 支持导出为 JSON/Markdown |

### 技术亮点

- 🚀 **现代化技术栈**：FastAPI + Vue 3 + Composition API
- 🔐 **JWT 认证**：安全的用户认证机制
- 📱 **响应式设计**：支持桌面端和移动端
- 🐳 **Docker 支持**：一键部署开发/生产环境
- 📖 **API 文档**：自动生成的 Swagger 文档

---

## 🛠️ 技术栈

### 后端

```
FastAPI 0.109.0      # 高性能 Web 框架
SQLAlchemy 2.0.25   # ORM
Alembic 1.13.1       # 数据库迁移
JWT                  # 用户认证
SQLite / PostgreSQL  # 数据库
```

### 前端

```
Vue 3.4              # 渐进式框架
Vite 5.4             # 构建工具
Pinia                # 状态管理
Vue Router           # 路由管理
Element Plus         # UI 组件库
```

---

## 🚀 快速开始

### 方式一：Docker（推荐）

```bash
# 克隆项目
git clone https://github.com/yourusername/pks.git
cd pks

# 配置环境变量
cp .env.docker.example .env
# 编辑 .env 文件，设置必要配置

# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 初始化数据库
docker-compose -f docker-compose.dev.yml exec backend python scripts/init_db.py
```

访问：
- 前端：http://localhost:5173
- 后端 API：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 方式二：本地开发

#### 后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境
cp .env.example .env

# 初始化数据库
python scripts/init_db.py

# 启动服务
uvicorn app.main:app --reload
```

#### 前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

---

## 📦 部署指南

### 生产环境（Docker）

```bash
# 配置生产环境变量
cp .env.docker.example .env
# 编辑 .env，设置强密码和域名

# 启动生产环境
docker-compose -f docker-compose.prod.yml up -d
```

### 生产环境（传统方式）

详细的部署指南请参考：[部署文档](docs/deployment.md)

---

## 📁 项目结构

```
pks/
├── backend/              # 后端服务（FastAPI）
│   ├── app/
│   │   ├── api/         # API 路由
│   │   ├── core/        # 核心配置
│   │   ├── models/      # 数据模型
│   │   ├── schemas/     # Pydantic 模式
│   │   ├── services/    # 业务逻辑
│   │   └── main.py      # 应用入口
│   ├── alembic/         # 数据库迁移
│   └── requirements.txt
│
├── frontend/             # 前端应用（Vue 3）
│   ├── src/
│   │   ├── api/         # API 调用
│   │   ├── components/  # 组件
│   │   ├── views/       # 页面视图
│   │   ├── router/      # 路由配置
│   │   ├── stores/      # 状态管理
│   │   └── main.js      # 应用入口
│   └── package.json
│
├── docs/                 # 项目文档
│   ├── architecture.md  # 架构设计
│   ├── data-model.md    # 数据模型
│   ├── api-design.md    # API 设计
│   └── deployment.md    # 部署指南
│
├── docker-compose.yml           # 完整环境
├── docker-compose.dev.yml       # 开发环境
├── docker-compose.prod.yml      # 生产环境
└── README.md
```

---

## 🔑 默认账号

首次运行需要注册账号，或使用以下测试账号（开发环境）：

```
用户名: admin
密码: password1
```

**⚠️ 生产环境请务必修改默认密码！**

---

## 📸 截图

### 登录页面
![登录页](docs/screenshots/login.png)

### 卡片管理
![卡片管理](docs/screenshots/cards.png)

### 看板视图
![看板视图](docs/screenshots/kanban.png)

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

请遵循 [代码规范](docs/CODING_STANDARDS.md)

---

## 📄 开源协议

本项目采用 [MIT](LICENSE) 协议开源。

---

## 📞 联系方式

- 作者：Your Name
- 邮箱：your.email@example.com
- 问题反馈：[GitHub Issues](https://github.com/yourusername/pks/issues)

---

## 🙏 致谢

感谢以下开源项目：

- [FastAPI](https://fastapi.tiangolo.com)
- [Vue.js](https://vuejs.org)
- [Vite](https://vitejs.dev)
- [Element Plus](https://element-plus.org)
- [SQLAlchemy](https://www.sqlalchemy.org)

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给一个 Star！**

Made with ❤️ by [Your Name](https://github.com/yourusername)

</div>
