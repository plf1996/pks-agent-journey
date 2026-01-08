# 🚀 AI-Agent 驱动的全栈项目实践：个人知识管理系统

<div align="center">

**探索 LLM 在复杂项目开发中的协同模式与边界**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Claude](https://img.shields.io/badge/Claude-Opus-orange.svg)](https://claude.ai/claude-code)

[项目成果](#项目成果) • [开发流程](#开发流程) • [核心发现](#核心发现) • [项目结构](#项目结构)

</div>

---

## 概述

本项目是一个**实验性探索项目**，旨在通过构建一个完整的个人知识管理系统（PKS），来验证和展示 **Claude Code** 在多角色 AI Agent 协同开发中的能力。

项目产出的不仅仅是代码，更是**对软件开发流程变革的深度思考**：当 AI 不再是辅助工具，而是能够承担架构设计、前端开发、后端实现等多个专业角色的协作伙伴时，我们的开发方式将如何演进？

---

## 项目成果

### 1. 完整的全栈应用

**PKS (Personal Knowledge System)** 是一个功能完整的个人知识管理系统：

| 模块 | 技术栈 | 功能描述 |
|------|--------|----------|
| **后端** | FastAPI + SQLAlchemy + Alembic | RESTful API、JWT 认证、数据库迁移 |
| **前端** | Vue 3 + Vite + Pinia + Element Plus | SPA 应用、状态管理、拖拽看板 |
| **数据库** | SQLite (开发) / PostgreSQL (生产) | 用户数据隔离、全文搜索索引 |
| **核心功能** | - | 知识卡片 CRUD、双向链接、全局搜索、看板管理、标签系统 |

完整的应用文档请查看 [`pks/README.md`](pks/README.md)

### 2. 完整的 AI 协作档案

本项目完整记录了与 AI 协同开发的全过程：

- **Agent 角色定义**: 架构师、前端专家、后端专家的角色描述和 Prompt 设计
- **对话日志**: 完整的交互历史，记录了需求分析、技术选型、代码实现的完整过程
- **决策过程**: 每个技术决策背后的讨论和思考路径

---

## 开发流程

### 传统开发模式 vs AI 协同模式

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           传统开发模式                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   产品需求 ──► 架构设计 ──► 前端开发 ──► 后端开发 ──► 联调测试 ──► 上线  │
│      │            │            │            │                          │
│      ▼            ▼            ▼            ▼                          │
│   (产品经理)   (架构师)     (前端工程师)  (后端工程师)                   │
│     3天          5天          10天         10天        总计: ~1个月     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         AI 协同开发模式                                  │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   产品需求 ──► 触发架构师 Agent ──► 并行触发前后端 Agent ──► 自动联调   │
│      │              │                     │                            │
│      ▼              ▼                     ▼                            │
│   (产品经理)   (software-architect)  (frontend + backend Agents)        │
│     3天            1小时                   并行执行      总计: ~1周      │
│                                                                         │
│   关键变革:                                                             │
│   • 角色从"人执行"变为"人监督 AI 执行"                                  │
│   • 并行协作替代串行等待                                                │
│   • 代码质量由 AI 自身的代码审查能力保证                                 │
│   • 人类聚焦于需求澄清和决策确认                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### 使用 Claude Code 的协作流程

```bash
# 1. 启动项目 - 架构师 Agent 设计系统架构
/plan 设计个人知识管理系统的架构

# 2. 并行开发 - 前后端 Agent 同时实现
# 终端 1: 后端开发
claude-code --agent backend-system-architect

# 终端 2: 前端开发
claude-code --agent frontend-dev-expert

# 3. 代码审查 - Agent 交叉审查
/review 请审查后端 API 的安全性

# 4. 联调测试 - 自动化测试集成
/test 运行集成测试
```

---

## 核心发现

### ✅ AI 协同的优势

1. **角色专业化**: 不同 Agent 具备明确的专业领域知识，能够提供领域级最佳实践
2. **并行执行能力**: 多个 Agent 可以同时工作，大幅缩短开发周期
3. **知识整合能力**: Agent 能够快速调用跨领域知识，避免"不知道自己不知道"
4. **代码一致性**: 统一的 Prompt 确保代码风格和架构决策的一致性

### ⚠️ 当前局限

1. **上下文窗口**: 超大项目仍需要分段处理，上下文切换存在信息损失
2. **隐性知识传递**: Agent 间的协作仍依赖人类作为"信息路由"
3. **创新边界**: Agent 更擅长实现已知模式，而非开创全新范式
4. **调试复杂性**: AI 生成的代码调试仍需要人类深入理解

### 🔮 未来展望

```
开发角色演进路径：

现在:
人类产品经理 ──► AI Agent ──► 代码仓库

未来 (3年内):
人类产品意图 ──► AI Product Manager ──► AI Team ──► 自动部署

更远 (5年+):
自然语言描述 ──► AI 全栈自主生成 ──► 实时部署迭代
```

---

## 项目结构

```
pks-agent-journey/
├── pks/                          # PKS 应用完整代码
│   ├── backend/                  # FastAPI 后端
│   ├── frontend/                 # Vue 3 前端
│   └── docs/                     # 架构设计文档
│
├── claude-code/                  # Claude Code 配置档案
│   ├── agents/                   # Agent 角色定义
│   │   ├── software-architect.md # 架构师 Agent Prompt
│   │   ├── backend-system-architect.md  # 后端专家 Agent Prompt
│   │   └── frontend-dev-expert.md       # 前端专家 Agent Prompt
│   │
│   └── skills/                   # 可复用技能定义
│
├── log/                          # 完整对话日志
│   └── history.txt               # ~100KB 的完整交互历史
│
├── Project Requirements.md       # 原始产品需求文档
├── CLAUDE.md                     # Claude Code 项目指南
└── README.md                     # 本文件
```

---

## Agent 角色设计

### software-architect (架构师)

**职责**: 将业务需求转化为技术架构方案

**核心能力**:
- 需求分析与技术转化
- 架构设计（分层架构、微服务、事件驱动）
- 技术选型与论证
- 风险评估与演进规划

**示例 Prompt**:
```
"我们需要设计一个高可用的电商平台，要支持每秒10,000订单，
需要考虑哪些架构层面的问题？"
```

### backend-system-architect (后端专家)

**职责**: 后端系统设计与实现

**核心能力**:
- API 设计与实现
- 数据库设计与优化
- 性能调优与安全防护
- 部署与运维

**示例 Prompt**:
```
"我需要设计一个订单处理系统，每秒需要处理大约1000个订单请求，
还需要保证数据一致性"
```

### frontend-dev-expert (前端专家)

**职责**: 前端架构与交互实现

**核心能力**:
- 组件架构设计
- 状态管理方案
- 性能优化
- 用户体验设计

**示例 Prompt**:
```
"我需要实现一个用户注册表单，包含邮箱验证、密码强度检测
和确认密码匹配功能"
```

---

## 对话日志分析

完整的对话日志位于 `log/history.txt`，记录了从项目启动到完成的完整过程。

### 关键里程碑

| 阶段 | Agent | 对话轮次 | 时间 | 产出 |
|------|-------|----------|------|------|
| 需求分析 | software-architect | 15 | ~20min | 架构设计文档 |
| 后端实现 | backend-system-architect | 45 | ~60min | 完整后端代码 |
| 前端实现 | frontend-dev-expert | 50 | ~70min | 完整前端代码 |
| 联调优化 | 多 Agent 协作 | 30 | ~40min | 集成测试通过 |

---

## 如何使用本项目

### 作为学习者

1. **阅读对话日志**: 了解 AI 如何思考和解决问题
2. **研究 Agent 定义**: 学习如何设计有效的 Prompt
3. **运行代码实践**: 体验最终产出的应用

### 作为开发者

1. **复刻 Agent 定义**: 在自己的项目中使用这些 Prompt
2. **参考协作模式**: 设计适合团队的 AI 协作流程
3. **贡献改进**: 提交你的 Agent 优化建议

### 运行 PKS 应用

```bash
# 后端
cd pks/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 前端
cd pks/frontend
npm install
npm run dev
```

详细文档请查看 [`pks/README.md`](pks/README.md)

---

## 技术栈

| 类别 | 技术 | 用途 |
|------|------|------|
| **AI 协作** | Claude Code | AI 编程助手 |
| **后端** | FastAPI | Web 框架 |
| **后端** | SQLAlchemy | ORM |
| **前端** | Vue 3 | 前端框架 |
| **前端** | Element Plus | UI 组件 |
| **数据库** | SQLite / PostgreSQL | 数据存储 |

---

## 开源协议

MIT License - 详见 [LICENSE](LICENSE)

---

## 致谢

### 开源项目

本项目使用以下优秀的开源项目：

- [FastAPI](https://fastapi.tiangolo.com/) - 现代化的 Python Web 框架
- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Claude Code](https://claude.ai/claude-code) - AI 编程助手

### Claude Code Skills

本项目使用了以下 Claude Code 技能扩展：

- [anthropics/skills](https://github.com/anthropics/skills) - Claude Code 官方技能集合，包含文档处理、前端设计、MCP 构建等众多实用技能
- [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files) - 使用持久化 Markdown 文件进行规划、进度跟踪和知识管理的技能，非常适合复杂项目的结构化协作

这些技能极大地扩展了 Claude Code 的能力边界，使得 AI Agent 能够更好地参与项目规划和文档管理。

### AI 模型与工具

本项目在开发过程中使用了以下 AI 服务：

- **[智谱 AI (GLM)](https://github.com/THUDM/GLM-4)** - 使用了最新的 GLM-4.7 模型及其提供的 MCP (Model Context Protocol) 工具，为项目提供了强大的中文理解和多模态能力支持

特别感谢智谱 AI 的 MCP 工具生态，让 AI Agent 能够更灵活地与外部工具和数据进行交互。

---

<div align="center">

**⭐ 如果这个项目对你有启发，请给一个 Star！**

Made with 🤖 by Human + AI Collaboration

</div>
