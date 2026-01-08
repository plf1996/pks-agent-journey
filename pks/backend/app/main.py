"""
FastAPI应用入口

个人知识管理系统（PKS）后端服务
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, cards, tags, links, search, kanban
import os
from pathlib import Path

# 创建FastAPI应用实例
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="个人知识管理系统 API",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(cards.router, prefix="/api/v1/cards", tags=["卡片"])
app.include_router(tags.router, prefix="/api/v1/tags", tags=["标签"])
app.include_router(links.router, prefix="/api/v1/cards", tags=["卡片链接"])
app.include_router(search.router, prefix="/api/v1/search", tags=["搜索"])
app.include_router(kanban.router, prefix="/api/v1/kanban", tags=["看板"])


@app.on_event("startup")
async def startup_event():
    """应用启动时自动初始化数据库"""
    from app.db.base import engine
    from sqlalchemy import inspect
    import subprocess
    import sys

    print("=" * 40)
    print("PKS Backend 启动中...")
    print("=" * 40)

    # 检查数据库是否需要初始化
    inspector = inspect(engine)

    if not inspector.has_table('alembic_version'):
        print("检测到数据库未初始化，开始自动初始化...")

        # 确保 alembic/versions 目录存在
        versions_dir = Path("/app/alembic/versions")
        if not versions_dir.exists():
            print(f"创建目录: {versions_dir}")
            versions_dir.mkdir(parents=True, exist_ok=True)

        # 运行 alembic 升级
        try:
            print("执行数据库迁移...")
            result = subprocess.run(
                [sys.executable, "-m", "alembic", "upgrade", "head"],
                capture_output=True,
                text=True,
                cwd="/app"
            )

            if result.returncode == 0:
                print("✓ 数据库迁移成功!")
            else:
                print(f"数据库迁移输出: {result.stdout}")
                if result.stderr:
                    print(f"错误: {result.stderr}")
        except Exception as e:
            print(f"数据库初始化警告: {e}")
            print("如果使用开发环境，可能需要手动运行: alembic upgrade head")
    else:
        print("✓ 数据库已初始化")

    print("=" * 40)
    print("PKS Backend 已启动!")
    print("=" * 40)


@app.get("/")
def root():
    """根路径"""
    return {
        "message": "欢迎使用个人知识管理系统 API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/api/health")
def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


@app.get("/api/v1")
def api_info():
    """API版本信息"""
    return {
        "name": "PKS API",
        "version": settings.APP_VERSION,
        "description": "个人知识管理系统 API",
        "documentation": "/docs"
    }


@app.get("/api/v1/health")
def health_check_v1():
    """健康检查（v1路径）"""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
