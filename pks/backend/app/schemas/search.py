"""
搜索相关的Pydantic模式
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.models.card import CardType


class SearchQuery(BaseModel):
    """搜索查询模式"""

    q: str = Field(..., min_length=1, description="搜索关键词")
    type: str = Field(default="all", pattern=r'^(all|cards|tags)$', description="搜索类型")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")


class AdvancedSearchRequest(BaseModel):
    """高级搜索请求模式"""

    keywords: str = Field(..., min_length=1, description="搜索关键词")
    card_types: Optional[List[CardType]] = Field(None, description="卡片类型筛选")
    tag_ids: Optional[List[int]] = Field(None, description="标签筛选")
    date_range: Optional[dict] = Field(None, description="日期范围")
    is_pinned: Optional[bool] = Field(None, description="是否置顶")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")


class SearchResultCard(BaseModel):
    """搜索结果卡片"""

    id: int
    title: str
    content: str
    card_type: CardType
    highlight: Optional[str] = None
    created_at: datetime

    class Config:
        """Pydantic配置"""
        from_attributes = True


class SearchResultTag(BaseModel):
    """搜索结果标签"""

    id: int
    name: str
    color: str
    cards_count: int

    class Config:
        """Pydantic配置"""
        from_attributes = True


class SearchResponse(BaseModel):
    """搜索响应模式"""

    cards: Optional[dict] = None
    tags: Optional[dict] = None
    total: int = 0


class ExportRequest(BaseModel):
    """导出请求模式"""

    card_ids: Optional[List[int]] = Field(None, description="卡片ID列表，为空则导出所有")
    include_links: bool = Field(default=True, description="是否包含链接")
    include_tags: bool = Field(default=True, description="是否包含标签")


class ExportResponse(BaseModel):
    """导出响应模式"""

    export_url: Optional[str] = None
    cards_count: int = 0
    file_size: int = 0
    expires_at: Optional[datetime] = None


class StatsResponse(BaseModel):
    """统计响应模式"""

    cards: dict = {}
    tags: dict = {}
    links: dict = {}
    activity: dict = {}
