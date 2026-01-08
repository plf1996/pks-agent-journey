"""
Alembic环境配置

用于数据库迁移
"""
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# 导入配置和模型
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.core.config import settings
from app.db.base import Base

# 导入所有模型以确保它们被注册到Base.metadata
from app.models import user, card, tag, link, kanban

# Alembic Config对象
config = context.config

# 设置数据库URL（从配置中获取）
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# 解释日志配置
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 设置模型的元数据
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    在'离线'模式下运行迁移

    这种方式不需要创建数据库连接，直接生成SQL脚本
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    在'在线'模式下运行迁移

    这种方式会创建数据库连接并执行迁移
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


# 根据上下文判断运行模式
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
