"""
PKS 数据模型
导入所有模型类以便 SQLAlchemy registry 可以正确解析关系
"""
from app.models.card import Card, CardType
from app.models.tag import Tag, CardTag
from app.models.link import CardLink, LinkType
from app.models.kanban import KanbanColumn, KanbanCard
from app.models.user import User

__all__ = [
    "User",
    "Card",
    "CardType",
    "Tag",
    "CardTag",
    "CardLink",
    "LinkType",
    "KanbanColumn",
    "KanbanCard",
]
