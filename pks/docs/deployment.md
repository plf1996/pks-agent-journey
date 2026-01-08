# 个人知识管理系统 (PKS) - 部署指南

## 目录
1. [系统要求](#系统要求)
2. [Docker 部署（推荐）](#docker-部署推荐)
3. [开发环境部署](#开发环境部署)
4. [生产环境部署](#生产环境部署)
5. [数据库配置](#数据库配置)
6. [反向代理配置](#反向代理配置)
7. [系统维护](#系统维护)

---

## 系统要求

### 最低配置

| 组件 | 要求 |
|------|------|
| 操作系统 | Linux / macOS / Windows |
| Python | 3.9 或更高版本 |
| Node.js | 16.0 或更高版本 |
| 内存 | 2GB 以上 |
| 磁盘 | 1GB 以上可用空间 |

### 推荐配置

| 组件 | 要求 |
|------|------|
| 操作系统 | Ubuntu 20.04+ / CentOS 8+ |
| Python | 3.10+ |
| Node.js | 18 LTS |
| 内存 | 4GB 以上 |
| 磁盘 | SSD，10GB 以上 |

---

## Docker 部署（推荐）

Docker 部署是最简单的方式，适合开发和生产环境。

### 前置要求

- Docker 20.10+
- Docker Compose 2.0+

### 需要的镜像

请提前下载以下镜像到本地（国内网络环境）：

```bash
# 后端运行环境
docker pull python:3.10-slim

# 前端构建环境
docker pull node:18-alpine

# 生产环境数据库
docker pull postgres:15-alpine

# Web服务器
docker pull nginx:alpine
```

### 快速启动

#### 1. 配置环境变量

```bash
cd /root/projects/pks

# 复制环境变量模板
cp .env.docker.example .env

# 编辑环境变量
nano .env
```

`.env` 文件配置示例：

```bash
# 应用配置
APP_NAME=PKS
APP_VERSION=1.0.0
DEBUG=false

# 安全配置
SECRET_KEY=请生成一个强随机密钥

# 数据库配置
POSTGRES_DB=pks_db
POSTGRES_USER=pks_user
POSTGRES_PASSWORD=请设置一个强密码

# CORS配置
BACKEND_CORS_ORIGINS=["http://localhost","http://localhost:80"]

# JWT配置
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### 2. 开发环境启动

使用 SQLite 数据库，无需 PostgreSQL：

```bash
# 启动开发环境
docker-compose -f docker-compose.dev.yml up -d

# 查看日志
docker-compose -f docker-compose.dev.yml logs -f

# 停止服务
docker-compose -f docker-compose.dev.yml down
```

访问地址：
- 前端：http://localhost:5173
- 后端API文档：http://localhost:8000/docs

#### 3. 生产环境启动

使用 PostgreSQL 数据库，完整的生产配置：

```bash
# 启动生产环境
docker-compose -f docker-compose.prod.yml up -d

# 查看日志
docker-compose -f docker-compose.prod.yml logs -f

# 查看特定服务日志
docker-compose -f docker-compose.prod.yml logs -f backend

# 停止服务
docker-compose -f docker-compose.prod.yml down

# 停止并删除数据卷（慎用）
docker-compose -f docker-compose.prod.yml down -v
```

访问地址：
- 前端：http://localhost
- 后端：内部网络，不直接暴露

#### 4. 完整环境启动（包含所有服务）

```bash
# 启动所有服务（PostgreSQL + 后端 + 前端）
docker-compose up -d

# 查看运行状态
docker-compose ps

# 查看日志
docker-compose logs -f
```

### Docker 常用命令

```bash
# 重新构建镜像
docker-compose build

# 重新构建并启动
docker-compose up -d --build

# 进入容器Shell
docker-compose exec backend /bin/bash
docker-compose exec frontend /bin/sh

# 在容器中执行命令
docker-compose exec backend python scripts/init_db.py

# 查看容器资源占用
docker stats

# 清理未使用的镜像和容器
docker system prune -a
```

### 数据持久化

Docker Compose 使用命名卷来持久化数据：

```bash
# 查看数据卷
docker volume ls | grep pks

# 备份数据卷
docker run --rm -v pks_postgres_data:/data -v $(pwd):/backup \
    alpine tar czf /backup/pks-postgres-backup.tar.gz -C /data .

# 恢复数据卷
docker run --rm -v pks_postgres_data:/data -v $(pwd):/backup \
    alpine tar xzf /backup/pks-postgres-backup.tar.gz -C /data
```

### 数据库初始化

首次启动后，需要初始化数据库：

```bash
# 方式1：进入容器执行
docker-compose exec backend python scripts/init_db.py

# 方式2：直接在主机执行（如果挂载了卷）
docker-compose exec backend alembic upgrade head
```

### 更新部署

```bash
# 停止服务
docker-compose down

# 拉取最新代码
git pull origin main

# 重新构建镜像
docker-compose build --no-cache

# 启动服务
docker-compose up -d
```

---

## 开发环境部署

### 1. 克隆项目

```bash
cd /path/to/projects
# 假设项目已存在于 /root/projects/pks
cd /root/projects/pks
```

### 2. 后端部署

#### 2.1 创建虚拟环境

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# Linux/macOS:
source venv/bin/activate
# Windows:
# venv\Scripts\activate
```

#### 2.2 安装依赖

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### 2.3 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件
nano .env
```

`.env` 文件配置示例：

```bash
# 应用配置
APP_NAME="PKS"
APP_VERSION="1.0.0"
DEBUG=True
SECRET_KEY=your-secret-key-change-this

# 数据库配置
DATABASE_URL=sqlite:///./pks.db

# CORS配置
BACKEND_CORS_ORIGINS=["http://localhost:5173","http://localhost:3000"]

# JWT配置
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### 2.4 初始化数据库

```bash
python scripts/init_db.py
```

#### 2.5 启动后端服务

```bash
# 方式1：使用启动脚本
./start_server.sh

# 方式2：直接使用 uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

后端服务启动后，访问以下地址：
- API文档：http://localhost:8000/docs
- ReDoc文档：http://localhost:8000/redoc

### 3. 前端部署

#### 3.1 安装依赖

```bash
cd ../frontend

# 如果无法使用 npm install，可以尝试使用国内镜像
npm install --registry=https://registry.npmmirror.com
```

#### 3.2 配置环境变量

编辑 `.env` 文件：

```bash
VITE_API_BASE_URL=http://localhost:8000/api/v1
VITE_APP_NAME=PKS
```

#### 3.3 启动开发服务器

```bash
npm run dev
```

前端服务启动后，访问：http://localhost:5173

### 4. 创建测试账号

```bash
# 使用 curl 创建测试用户
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "email": "admin@example.com",
    "password": "Admin123!"
  }'
```

---

## 生产环境部署

### 方案一：Docker 部署（推荐）

Docker 部署是最简单可靠的方式，详见上文 [Docker 部署](#docker-部署推荐) 章节。

```bash
# 生产环境快速启动
cd /root/projects/pks
docker-compose -f docker-compose.prod.yml up -d
```

### 方案二：传统部署（适合无 Docker 环境）

此方案不需要 Docker，适合国内网络环境。

#### 1. 准备服务器

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装必要软件
sudo apt install -y python3 python3-pip python3-venv nginx nodejs npm
```

#### 2. 部署后端

```bash
# 创建项目目录
sudo mkdir -p /opt/pks
sudo chown $USER:$USER /opt/pks

# 复制后端代码
cp -r /root/projects/pks/backend /opt/pks/

# 进入后端目录
cd /opt/pks/backend

# 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 生产环境额外依赖
pip install gunicorn
```

#### 3. 配置生产环境变量

```bash
cp .env.example .env
nano .env
```

生产环境 `.env` 配置：

```bash
# 应用配置
APP_NAME="PKS"
APP_VERSION="1.0.0"
DEBUG=False
SECRET_KEY=请生成一个强随机密钥

# 数据库配置（生产环境建议使用 PostgreSQL）
DATABASE_URL=postgresql://user:password@localhost/pks_db

# CORS配置（设置为实际域名）
BACKEND_CORS_ORIGINS=["https://your-domain.com"]

# JWT配置
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

生成强密钥：

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### 4. 初始化数据库

```bash
source venv/bin/activate
python scripts/init_db.py
```

#### 5. 配置 Gunicorn 服务

创建 Systemd 服务文件：

```bash
sudo nano /etc/systemd/system/pks-backend.service
```

内容如下：

```ini
[Unit]
Description=PKS Backend Service
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/opt/pks/backend
Environment="PATH=/opt/pks/backend/venv/bin"
ExecStart=/opt/pks/backend/venv/bin/gunicorn \
    -k uvicorn.workers.UvicornWorker \
    -w 4 \
    -b 127.0.0.1:8000 \
    --access-logfile /var/log/pks/access.log \
    --error-logfile /var/log/pks/error.log \
    app.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

创建日志目录：

```bash
sudo mkdir -p /var/log/pks
sudo chown www-data:www-data /var/log/pks
```

启动服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable pks-backend
sudo systemctl start pks-backend
sudo systemctl status pks-backend
```

#### 6. 部署前端

```bash
# 复制前端代码
cp -r /root/projects/pks/frontend /opt/pks/

# 进入前端目录
cd /opt/pks/frontend

# 安装依赖
npm install --registry=https://registry.npmmirror.com

# 构建生产版本
npm run build
```

构建产物在 `dist/` 目录中。

#### 7. 配置 Nginx

创建 Nginx 配置：

```bash
sudo nano /etc/nginx/sites-available/pks
```

内容如下：

```nginx
# 后端 API 代理
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# 前端静态文件
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    root /opt/pks/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # API 代理（可选：如果前后端在同一域名）
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 静态资源缓存
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

启用站点：

```bash
sudo ln -s /etc/nginx/sites-available/pks /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

#### 8. 配置 HTTPS（使用 Let's Encrypt）

```bash
# 安装 certbot
sudo apt install certbot python3-certbot-nginx

# 获取证书
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# 自动续期
sudo certbot renew --dry-run
```

---

## 数据库配置

### SQLite（开发/小规模部署）

默认配置，无需额外设置。数据库文件位于 `backend/pks.db`。

### PostgreSQL（生产环境推荐）

#### 1. 安装 PostgreSQL

```bash
sudo apt install postgresql postgresql-contrib
```

#### 2. 创建数据库和用户

```bash
sudo -u postgres psql
```

```sql
-- 创建数据库
CREATE DATABASE pks_db;

-- 创建用户
CREATE USER pks_user WITH PASSWORD 'your-strong-password';

-- 授权
GRANT ALL PRIVILEGES ON DATABASE pks_db TO pks_user;

-- 退出
\q
```

#### 3. 更新后端配置

修改 `.env` 文件：

```bash
DATABASE_URL=postgresql://pks_user:your-strong-password@localhost/pks_db
```

#### 4. 运行迁移

```bash
cd /opt/pks/backend
source venv/bin/activate
alembic upgrade head
```

---

## 反向代理配置

### Nginx 常用配置

#### 限制请求大小

```nginx
client_max_body_size 10M;
```

#### 超时设置

```nginx
proxy_connect_timeout 60s;
proxy_send_timeout 60s;
proxy_read_timeout 60s;
```

#### WebSocket 支持（如需）

```nginx
proxy_http_version 1.1;
proxy_set_header Upgrade $http_upgrade;
proxy_set_header Connection "upgrade";
```

---

## 系统维护

### 日志查看

```bash
# 后端日志
sudo tail -f /var/log/pks/error.log

# Nginx 日志
sudo tail -f /var/log/nginx/error.log

# Systemd 日志
sudo journalctl -u pks-backend -f
```

### 数据备份

```bash
# SQLite 备份
cp /opt/pks/backend/pks.db /backup/pks-$(date +%Y%m%d).db

# PostgreSQL 备份
pg_dump -U pks_user pks_db > /backup/pks-$(date +%Y%m%d).sql
```

### 更新部署

```bash
# 停止服务
sudo systemctl stop pks-backend

# 更新代码
cd /opt/pks/backend
git pull origin main  # 或复制新代码

# 激活虚拟环境
source venv/bin/activate

# 更新依赖
pip install -r requirements.txt

# 运行迁移
alembic upgrade head

# 重启服务
sudo systemctl start pks-backend
```

### 监控

推荐安装以下工具：

```bash
# 系统监控
sudo apt install htop

# Nginx 访客统计
# 可使用 GoAccess 或其他日志分析工具
```

---

## 故障排查

### 后端无法启动

1. 检查端口是否被占用：
```bash
sudo lsof -i :8000
```

2. 检查日志：
```bash
sudo journalctl -u pks-backend -n 50
```

3. 检查数据库连接：
```bash
python -c "from app.db.session import engine; print(engine.connect())"
```

### 前端无法访问后端

1. 检查 CORS 配置
2. 检查 API 地址配置
3. 检查防火墙规则

### 数据库错误

1. 检查数据库文件权限
2. 检查数据库连接字符串
3. 运行数据库迁移

---

## 安全建议

1. **定期更新**：保持系统和依赖包最新
2. **强密码**：使用强密码和密钥
3. **防火墙**：配置适当的防火墙规则
4. **备份**：定期备份数据库
5. **HTTPS**：生产环境必须使用 HTTPS
6. **日志审计**：定期检查访问日志

---

## 联系支持

如有部署问题，请联系：
- 邮件：support@example.com
- Issue：项目 GitHub 仓库

---

**版本**：v1.0.0
**更新日期**：2025-01-08
