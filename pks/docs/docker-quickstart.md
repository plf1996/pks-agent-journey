# PKS Docker 部署快速参考

## 需要的镜像

请提前下载以下镜像：

```bash
docker pull python:3.10-slim      # 后端运行环境
docker pull node:18-alpine         # 前端构建环境
docker pull postgres:15-alpine     # 生产数据库
docker pull nginx:alpine           # Web服务器
```

## 配置文件说明

| 文件 | 用途 |
|------|------|
| `docker-compose.yml` | 完整环境配置 |
| `docker-compose.dev.yml` | 开发环境（SQLite） |
| `docker-compose.prod.yml` | 生产环境（PostgreSQL） |
| `backend/Dockerfile` | 后端镜像构建 |
| `frontend/Dockerfile` | 前端生产镜像 |
| `frontend/Dockerfile.dev` | 前端开发镜像 |
| `.env.docker.example` | 环境变量模板 |

## 快速启动命令

### 开发环境

```bash
# 1. 配置环境变量
cp .env.docker.example .env
nano .env  # 修改配置

# 2. 启动服务
docker-compose -f docker-compose.dev.yml up -d

# 3. 查看日志
docker-compose -f docker-compose.dev.yml logs -f

# 4. 初始化数据库
docker-compose -f docker-compose.dev.yml exec backend python scripts/init_db.py
```

### 生产环境

```bash
# 1. 配置环境变量（重要：设置强密码）
cp .env.docker.example .env
nano .env  # 修改 SECRET_KEY 和 POSTGRES_PASSWORD

# 2. 启动服务
docker-compose -f docker-compose.prod.yml up -d

# 3. 查看状态
docker-compose -f docker-compose.prod.yml ps

# 4. 初始化数据库
docker-compose -f docker-compose.prod.yml exec backend python scripts/init_db.py
```

## 常用操作

```bash
# 停止服务
docker-compose -f docker-compose.dev.yml down

# 重新构建
docker-compose -f docker-compose.dev.yml build --no-cache
docker-compose -f docker-compose.dev.yml up -d

# 进入后端容器
docker-compose -f docker-compose.dev.yml exec backend /bin/bash

# 查看特定服务日志
docker-compose -f docker-compose.dev.yml logs -f backend
docker-compose -f docker-compose.dev.yml logs -f frontend

# 数据库迁移
docker-compose -f docker-compose.dev.yml exec backend alembic upgrade head

# 创建管理员用户
docker-compose -f docker-compose.dev.yml exec backend python -c "
from app.core.security import create_password_hash
print(create_password_hash('admin123'))
"
```

## 端口说明

| 端口 | 服务 | 环境 |
|------|------|------|
| 80 | 前端（Nginx） | 生产 |
| 5173 | 前端（Vite） | 开发 |
| 8000 | 后端API | 开发/生产（内部） |
| 5432 | PostgreSQL | 生产（内部） |

## 数据备份

```bash
# 备份 PostgreSQL 数据卷
docker run --rm \
  -v pks_postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/pks-backup-$(date +%Y%m%d).tar.gz -C /data .

# 恢复数据
docker run --rm \
  -v pks_postgres_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/pks-backup-20250108.tar.gz -C /data
```

## 故障排查

```bash
# 查看所有容器状态
docker ps -a

# 查看容器日志
docker logs pks-backend
docker logs pks-frontend

# 进入容器调试
docker exec -it pks-backend /bin/bash

# 检查网络连接
docker network ls
docker network inspect pks_pks-network

# 重启单个服务
docker-compose restart backend

# 清理并重建
docker-compose down -v
docker-compose up -d --build
```

## 环境变量参考

```bash
# .env 文件内容
APP_NAME=PKS
APP_VERSION=1.0.0
DEBUG=false

# 安全（必须修改）
SECRET_KEY=请生成强随机密钥

# 数据库（生产环境）
POSTGRES_DB=pks_db
POSTGRES_USER=pks_user
POSTGRES_PASSWORD=请设置强密码

# CORS
BACKEND_CORS_ORIGINS=["http://localhost","http://localhost:80"]

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 前端
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 访问地址

启动后访问：

| 环境 | 前端地址 | API文档 |
|------|----------|---------|
| 开发 | http://localhost:5173 | http://localhost:8000/docs |
| 生产 | http://localhost | http://localhost/api/docs |
