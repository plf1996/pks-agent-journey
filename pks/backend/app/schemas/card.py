"""
卡片相关的Pydantic模式
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field, validator
from app.models.card import CardType


class TagBase(BaseModel):
    """标签基础模式"""

    id: int
    name: str
    color: str

    class Config:
        """Pydantic配置"""
        from_attributes = True


class CardLinkInfo(BaseModel):
    """卡片链接信息"""

    id: int
    title: str
    link_type: str

    class Config:
        """Pydantic配置"""
        from_attributes = True


class CardBase(BaseModel):
    """卡片基础模式"""

    title: str = Field(..., min_length=1, max_length=200, description="卡片标题")
    content: str = Field(..., min_length=1, description="卡片内容")
    card_type: CardType = Field(default=CardType.NOTE, description="卡片类型")
    url: Optional[str] = Field(None, max_length=500, description="网页链接")


class CardCreate(CardBase):
    """卡片创建模式"""

    tag_ids: Optional[List[int]] = Field(default=[], description="标签ID列表")
    link_ids: Optional[List[int]] = Field(default=[], description="关联卡片ID列表")

    @validator('url')
    def validate_url(cls, v, values):
        """验证链接类型卡片必须提供URL"""
        if values.get('card_type') == CardType.LINK and not v:
            raise ValueError('链接类型卡片必须提供URL')
        return v


class CardUpdate(BaseModel):
    """卡片更新模式"""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    card_type: Optional[CardType] = None
    url: Optional[str] = Field(None, max_length=500)
    is_pinned: Optional[bool] = None
    tag_ids: Optional[List[int]] = None


class CardResponse(CardBase):
    """卡片响应模式"""

    id: int
    user_id: int
    is_pinned: bool
    view_count: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagBase] = []

    class Config:
        """Pydantic配置"""
        from_attributes = True


class CardDetailResponse(CardResponse):
    """卡片详情响应模式"""

    links: Optional[dict] = None  # {"outgoing": [], "incoming": []}


class CardListResponse(BaseModel):
    """卡片列表响应模式"""

    id: int
    title: str
    content: str
    card_type: CardType
    url: Optional[str]
    is_pinned: bool
    view_count: int
    tags: List[TagBase] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic配置"""
        from_attributes = True


class BatchDeleteRequest(BaseModel):
    """批量删除请求模式"""

    card_ids: List[int] = Field(..., min_length=1, description="卡片ID列表")


class BatchDeleteResponse(BaseModel):
    """批量删除响应模式"""

    deleted_count: int = Field(..., description="删除的卡片数量")


class BatchTagRequest(BaseModel):
    """批量打标签请求模式"""

    card_ids: List[int] = Field(..., min_length=1, description="卡片ID列表")
    tag_ids: List[int] = Field(..., min_length=1, description="标签ID列表")


class BatchTagResponse(BaseModel):
    """批量打标签响应模式"""

    affected_count: int = Field(..., description="影响的卡片数量")
