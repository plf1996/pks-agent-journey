#!/bin/bash

# 启动PKS Backend服务

echo "正在启动 PKS Backend 服务..."

# 激活虚拟环境
source venv/bin/activate

# 启动服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
