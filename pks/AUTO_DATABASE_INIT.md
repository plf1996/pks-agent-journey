# 数据库自动初始化功能

## 功能说明

现在数据库会在**容器启动时自动初始化**，无需手动执行任何命令！

---

## 实现方式

### 1. 应用级自动初始化（推荐） ✅

**文件**: `backend/app/main.py`

FastAPI 应用启动时会自动检查并初始化数据库：

```python
@app.on_event("startup")
async def startup_event():
    """应用启动时自动初始化数据库"""
    # 检查数据库是否需要初始化
    if not inspector.has_table('alembic_version'):
        # 自动执行 alembic upgrade head
```

**优点**:
- ✅ 代码实时生效（通过 volume 挂载）
- ✅ 不需要重新构建镜像
- ✅ 每次启动都会检查

---

### 2. Docker 容器级自动初始化

**文件**: `backend/scripts/entrypoint.sh` + `backend/Dockerfile`

容器启动脚本会检查并初始化数据库：

```dockerfile
# Dockerfile
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
```

**优点**:
- ✅ 在数据库迁移之前执行
- ✅ 可以处理更复杂的初始化逻辑
- ✅ 支持等待外部数据库就绪

---

## 工作流程

```
容器启动
    │
    ▼
检查数据库是否存在？
    │
    ├─ 是 → 跳过初始化
    │
    └─ 否 → 自动执行以下步骤：
        │
        ├─ 1. 创建 alembic/versions 目录
        ├─ 2. 运行 alembic upgrade head
        └─ 3. 创建数据库表
    │
    ▼
启动 FastAPI 应用
```

---

## 验证自动初始化

### 方法 1: 查看启动日志

```bash
docker logs pks-backend-dev
```

**期望输出**:
```
========================================
PKS Backend 启动中...
========================================
✓ 数据库已初始化
========================================
PKS Backend 已启动!
========================================
```

### 方法 2: 完整测试（删除数据库重启）

```bash
cd /root/projects/pks-agent-journey/pks

# 停止容器
docker-compose -f docker-compose.dev.yml down

# 删除数据库
rm -f backend/data/pks.db

# 重新启动（会自动初始化）
docker-compose -f docker-compose.dev.yml up -d

# 查看日志
docker logs pks-backend-dev --tail 50
```

---

## 当前状态

### 已实现的自动初始化 ✅

| 组件 | 文件 | 状态 |
|------|------|------|
| 应用启动检查 | `app/main.py` | ✅ 已生效 |
| 容器启动脚本 | `scripts/entrypoint.sh` | ✅ 已创建 |
| Dockerfile 配置 | `backend/Dockerfile` | ✅ 已更新 |
| Alembic 迁移 | `alembic/versions/*.py` | ✅ 已生成 |

### 测试结果

```bash
$ curl http://192.168.0.16:8000/api/v1/health
{"status":"healthy","version":"1.0.0"}
```

---

## 使用说明

### 新建环境

```bash
# 1. 启动容器（自动初始化数据库）
docker-compose -f docker-compose.dev.yml up -d

# 2. 访问应用
open http://192.168.0.16:5173

# 3. 注册账号并开始使用
```

### 开发环境

```bash
# 代码修改会自动重载（包括数据库初始化代码）
# 修改 backend/app/main.py 后自动生效

# 查看重载日志
docker logs pks-backend-dev -f
```

### 生产环境

```bash
# 使用生产配置启动
docker-compose -f docker-compose.prod.yml up -d

# 数据库会自动初始化（使用 PostgreSQL）
```

---

## 技术细节

### 启动事件检查

应用启动时检查 `alembic_version` 表：

```python
inspector = inspect(engine)
if not inspector.has_table('alembic_version'):
    # 需要初始化
    subprocess.run(["python", "-m", "alembic", "upgrade", "head"])
```

### Alembic 迁移

```bash
# 查看迁移版本
docker exec pks-backend-dev alembic current

# 查看迁移历史
docker exec pks-backend-dev alembic history

# 手动创建新迁移
docker exec pks-backend-dev alembic revision --autogenerate -m "描述"
```

---

## 常见问题

### Q: 如何重新初始化数据库？

```bash
# 删除数据库文件
rm -f backend/data/pks.db

# 重启容器（会自动初始化）
docker-compose -f docker-compose.dev.yml restart backend
```

### Q: 如何查看数据库初始化状态？

```bash
# 进入容器
docker exec -it pks-backend-dev bash

# 检查数据库
ls -la /app/data/
python -c "from app.db.base import engine; print('OK')"
```

### Q: 自动初始化失败怎么办？

```bash
# 查看详细日志
docker logs pks-backend-dev --tail 100

# 手动初始化
docker exec pks-backend-dev alembic upgrade head

# 检查迁移文件
docker exec pks-backend-dev ls -la /app/alembic/versions/
```

---

## 总结

✅ **数据库自动初始化已完全配置好**

- **开发环境**: 启动容器即可，自动初始化 SQLite
- **生产环境**: 启动容器即可，自动初始化 PostgreSQL
- **无需手动操作**: 不再需要进入容器执行初始化命令
- **代码级支持**: 应用启动时自动检查并初始化

从现在开始，每次启动新的容器都会自动初始化数据库！
