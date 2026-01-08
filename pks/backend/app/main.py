"""
FastAPI应用入口

个人知识管理系统（PKS）后端服务
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1 import auth, cards, tags, links, search, kanban

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
    allow_origins=settings.BACKEND_CORS_ORIGINS,
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
