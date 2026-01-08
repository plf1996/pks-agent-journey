# 贡献指南

感谢您对 PKS 个人知识管理系统的关注！我们欢迎任何形式的贡献。

## 🤝 如何贡献

### 报告问题

如果您发现了 Bug 或有功能建议：

1. 在 [Issues](https://github.com/yourusername/pks/issues) 中搜索是否已有相似问题
2. 如果没有，创建新的 Issue，详细描述问题或建议

### 提交代码

1. **Fork** 本仓库到您的 GitHub 账号
2. **克隆** 您的 Fork 到本地：
   ```bash
   git clone https://github.com/yourusername/pks.git
   cd pks
   ```
3. **创建** 分支：
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **进行** 您的更改
5. **提交** 更改：
   ```bash
   git commit -m "Add some feature"
   ```
6. **推送** 到您的 Fork：
   ```bash
   git push origin feature/your-feature-name
   ```
7. **创建** Pull Request 到本仓库

## 📋 开发规范

### 代码风格

#### 后端（Python）

- 遵循 PEP 8 规范
- 使用类型提示
- 函数和类添加文档字符串
- 变量命名使用 snake_case

```python
def create_user(db: Session, username: str) -> User:
    """创建新用户

    Args:
        db: 数据库会话
        username: 用户名

    Returns:
        创建的用户对象
    """
    pass
```

#### 前端（Vue.js）

- 组件命名使用 PascalCase
- 变量命名使用 camelCase
- 常量命名使用 UPPER_SNAKE_CASE
- 使用 Composition API

```javascript
// 组件文件名: CardList.vue
export default {
  name: 'CardList'
}
```

### 提交信息规范

使用清晰的提交信息格式：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**类型 (type)：**
- `feat`: 新功能
- `fix`: 修复 Bug
- `docs`: 文档更新
- `style`: 代码格式（不影响代码运行）
- `refactor`: 重构
- `test`: 测试
- `chore`: 构建过程或辅助工具的变动

**示例：**
```
feat(cards): 添加卡片批量删除功能

- 支持选择多个卡片进行删除
- 添加删除确认对话框
- 更新 API 接口

Closes #123
```

## 🧪 测试

在提交 PR 前，请确保：

- [ ] 代码通过 lint 检查
- [ ] 所有测试通过
- [ ] 新功能添加了相应测试
- [ ] 文档已更新

## 📝 PR 模板

提交 Pull Request 时，请填写以下信息：

```markdown
## 描述
简要描述此 PR 的目的和内容

## 类型
- [ ] Bug 修复
- [ ] 新功能
- [ ] 重构
- [ ] 文档更新
- [ ] 其他（请说明）

## 测试
描述您如何测试这些更改

## 截图
如果适用，添加截图展示更改

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 已进行自我审查
- [ ] 已添加必要的文档
- [ ] 已更新相关文档
```

## 📧 联系方式

如有疑问，请通过以下方式联系：

- Email: your.email@example.com
- GitHub Issues: https://github.com/yourusername/pks/issues

---

再次感谢您的贡献！🎉
