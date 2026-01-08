"""
数据库初始化脚本

创建初始迁移文件并执行
"""
import os
import sys

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from alembic.config import Config
from alembic import command


def init_database():
    """初始化数据库"""
    # 获取alembic配置
    alembic_cfg = Config(os.path.join(os.path.dirname(os.path.dirname(__file__)), "alembic.ini"))

    # 创建迁移脚本
    print("正在创建数据库迁移脚本...")
    command.revision(alembic_cfg, autogenerate=True, message="initial_schema")

    # 执行迁移
    print("正在执行数据库迁移...")
    command.upgrade(alembic_cfg, "head")

    print("数据库初始化完成!")


if __name__ == "__main__":
    init_database()
