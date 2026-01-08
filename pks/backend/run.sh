#!/bin/bash

# PKS Backend 启动脚本

echo "======================================"
echo "PKS Backend - 个人知识管理系统后端"
echo "======================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到Python3"
    exit 1
fi

echo "1. 创建虚拟环境..."
python3 -m venv venv

echo "2. 激活虚拟环境并安装依赖..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "3. 复制环境变量配置文件..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "已创建 .env 文件，请根据需要修改配置"
fi

echo "4. 初始化数据库..."
python scripts/init_db.py

echo ""
echo "======================================"
echo "安装完成！"
echo "======================================"
echo ""
echo "启动服务："
echo "  方式1: 使用启动脚本"
echo "    ./start_server.sh"
echo ""
echo "  方式2: 手动启动"
echo "    source venv/bin/activate"
echo "    uvicorn app.main:app --reload"
echo ""
echo "API文档地址："
echo "  http://localhost:8000/docs"
echo ""
