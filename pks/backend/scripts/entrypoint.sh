#!/bin/bash
# ============================================
# PKS Backend 容器启动脚本
# 功能：自动初始化数据库并启动服务
# ============================================

set -e

echo "================================"
echo "PKS Backend 容器启动"
echo "================================"

# 等待数据库就绪（如果是 PostgreSQL）
if [ "$DATABASE_URL" != "sqlite:///./data/pks.db" ]; then
    echo "等待 PostgreSQL 数据库就绪..."
    while ! python -c "from sqlalchemy import create_engine; engine = create_engine('$DATABASE_URL'); conn = engine.connect(); conn.close()" 2>/dev/null; do
        echo "数据库未就绪，等待 2 秒..."
        sleep 2
    done
    echo "数据库已就绪!"
fi

# 检查数据库是否需要初始化
echo "检查数据库状态..."

# 对于 SQLite，检查数据库文件是否存在
if [[ "$DATABASE_URL" == sqlite* ]]; then
    DB_FILE="/app/data/pks.db"
    if [ ! -f "$DB_FILE" ]; then
        echo "数据库文件不存在，创建数据库目录..."
        mkdir -p /app/data
        touch "$DB_FILE"
    fi
fi

# 检查 alembic 版本表是否存在（无论什么数据库）
NEED_INIT=0
python -c "
from app.db.session import engine
from sqlalchemy import inspect, text

inspector = inspect(engine)
if inspector.has_table('alembic_version'):
    # 检查是否有迁移记录
    with engine.connect() as conn:
        result = conn.execute(text('SELECT COUNT(*) FROM alembic_version'))
        count = result.scalar()
        if count == 0:
            exit(1)  # 需要初始化
    exit(0)  # 已初始化
else:
    exit(1)  # 需要初始化
" 2>/dev/null || NEED_INIT=1

if [ $NEED_INIT -eq 1 ]; then
    echo "数据库未初始化，开始初始化..."

    # 确保 alembic/versions 目录存在
    if [ ! -d "/app/alembic/versions" ]; then
        echo "创建 alembic/versions 目录..."
        mkdir -p /app/alembic/versions
    fi

    # 检查是否有迁移文件
    if [ -z "$(ls -A /app/alembic/versions)" ]; then
        echo "创建初始数据库迁移..."
        alembic revision --autogenerate -m "initial_schema"
    fi

    echo "执行数据库迁移..."
    alembic upgrade head

    echo "数据库初始化完成!"
else
    echo "数据库已初始化，跳过。"
fi

# 初始化默认看板列（如果需要）
echo "检查看板配置..."
python -c "
from app.db.session import SessionLocal
from app.services.kanban_service import KanbanService
from app.models.user import User

db = SessionLocal()
try:
    # 获取第一个用户
    user = db.query(User).first()
    if user:
        KanbanService.init_default_columns(db, user.id)
        print('看板配置检查完成')
    else:
        print('暂无用户，跳过看板初始化')
finally:
    db.close()
"

echo "================================"
echo "启动 FastAPI 服务器..."
echo "================================"

# 启动应用
exec "$@"
