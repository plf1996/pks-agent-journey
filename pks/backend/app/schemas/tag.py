"""
标签相关的Pydantic模式
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.tag import Tag


class TagBase(BaseModel):
    """标签基础模式"""

    name: str = Field(..., min_length=1, max_length=50, description="标签名称")
    color: str = Field(default="#1976D2", pattern=r'^#[0-9A-Fa-f]{6}$', description="标签颜色")
    parent_id: Optional[int] = Field(None, description="父标签ID")


class TagCreate(TagBase):
    """标签创建模式"""

    pass


class TagUpdate(BaseModel):
    """标签更新模式"""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    color: Optional[str] = Field(None, pattern=r'^#[0-9A-Fa-f]{6}$')


class TagResponse(TagBase):
    """标签响应模式"""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic配置"""
        from_attributes = True


class TagDetailResponse(TagResponse):
    """标签详情响应模式"""

    children: List['TagResponse'] = []
    cards_count: int = 0


class TagWithCount(TagResponse):
    """带统计信息的标签响应模式"""

    children_count: int = 0
    cards_count: int = 0
