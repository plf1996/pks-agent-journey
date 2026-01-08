"""
看板相关的Pydantic模式
"""
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field


class KanbanColumnBase(BaseModel):
    """看板列基础模式"""

    name: str = Field(..., min_length=1, max_length=50, description="列名称")
    position: int = Field(..., ge=0, description="位置")


class KanbanColumnCreate(KanbanColumnBase):
    """看板列创建模式"""

    pass


class KanbanColumnUpdate(BaseModel):
    """看板列更新模式"""

    name: Optional[str] = Field(None, min_length=1, max_length=50)
    position: Optional[int] = Field(None, ge=0)


class KanbanColumnResponse(KanbanColumnBase):
    """看板列响应模式"""

    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic配置"""
        from_attributes = True


class KanbanCardBase(BaseModel):
    """看板卡片基础模式"""

    card_id: int = Field(..., description="卡片ID")
    column_id: int = Field(..., description="列ID")
    position: int = Field(..., ge=0, description="位置")


class KanbanCardResponse(KanbanCardBase):
    """看板卡片响应模式"""

    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic配置"""
        from_attributes = True


class KanbanColumnWithCards(KanbanColumnResponse):
    """包含卡片的看板列响应模式"""

    cards_count: int = 0
    cards: List[dict] = []


class MoveCardRequest(BaseModel):
    """移动卡片请求模式"""

    card_id: int = Field(..., description="卡片ID")
    column_id: int = Field(..., description="目标列ID")
    position: int = Field(..., ge=0, description="位置")


class MoveCardResponse(BaseModel):
    """移动卡片响应模式"""

    card_id: int
    column_id: int
    position: int


class BatchMoveRequest(BaseModel):
    """批量移动卡片请求模式"""

    card_ids: List[int] = Field(..., min_length=1, description="卡片ID列表")
    target_column_id: int = Field(..., description="目标列ID")


class BatchMoveResponse(BaseModel):
    """批量移动卡片响应模式"""

    moved_count: int = Field(..., description="移动的卡片数量")


class KanbanBoardResponse(BaseModel):
    """看板板响应模式"""

    columns: List[KanbanColumnWithCards] = []
