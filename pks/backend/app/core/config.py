"""
核心配置模块

包含应用的所有配置项，使用环境变量进行配置
"""
import os
import json
from typing import Optional, Union
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """应用配置类"""

    # 应用基础配置
    APP_NAME: str = "Personal Knowledge System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API配置
    API_V1_PREFIX: str = "/api/v1"

    # 数据库配置
    # 开发环境使用SQLite，生产环境可切换到PostgreSQL
    DATABASE_URL: str = "sqlite:///./pks.db"
    # PostgreSQL示例: postgresql+asyncpg://user:password@localhost/pks

    # JWT配置
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120  # 2小时
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30  # 30天

    # CORS配置 - 支持JSON字符串或列表
    BACKEND_CORS_ORIGINS: Union[str, list[str]] = [
        "http://localhost:5173",  # Vite默认端口
        "http://localhost:3000",  # React默认端口
        "http://localhost:8080",  # Vue CLI默认端口
        "http://192.168.0.16:5173",  # 虚拟机访问
        "http://192.168.0.16",  # 虚拟机访问
    ]

    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100

    # 文件上传配置
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"

    # 搜索配置
    SEARCH_RESULTS_LIMIT: int = 50

    @property
    def cors_origins(self) -> list[str]:
        """解析CORS配置，支持JSON字符串或列表"""
        if isinstance(self.BACKEND_CORS_ORIGINS, str):
            try:
                return json.loads(self.BACKEND_CORS_ORIGINS)
            except json.JSONDecodeError:
                return [self.BACKEND_CORS_ORIGINS]
        return self.BACKEND_CORS_ORIGINS

    class Config:
        """Pydantic配置"""
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    获取配置单例

    使用lru_cache确保配置只加载一次
    """
    return Settings()


# 全局配置实例
settings = get_settings()
