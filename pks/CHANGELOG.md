# 更新日志

所有重要更改都将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)，
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

### 计划功能
- [ ] 卡片版本历史
- [ ] 多人协作
- [ ] 知识图谱可视化
- [ ] WebDAV 同步
- [ ] 移动端 App

## [1.0.0] - 2025-01-08

### 新增
- ✨ 用户注册/登录功能
- ✨ JWT 身份认证
- ✨ 知识卡片 CRUD 操作
- ✨ 四种卡片类型：笔记、链接、图片、代码
- ✨ 双向链接功能
- ✨ 全局搜索功能
- ✨ 标签系统（支持层级结构）
- ✨ 看板视图（拖拽管理）
- ✨ 批量操作功能
- ✨ 数据导出（JSON/Markdown）
- ✨ 响应式设计
- ✨ Docker 部署支持
- ✨ Swagger API 文档

### 技术栈
- 后端：FastAPI + SQLAlchemy + SQLite/PostgreSQL
- 前端：Vue 3 + Vite + Pinia + Element Plus

---

## 版本说明

### 主版本号 (Major)：不兼容的 API 修改
### 次版本号 (Minor)：向下兼容的功能性新增
### 修订号 (Patch)：向下兼容的问题修正
