"""
卡片数据模型
"""
import enum
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class CardType(str, enum.Enum):
    """卡片类型枚举"""
    NOTE = "note"      # 笔记
    LINK = "link"      # 网页链接
    IMAGE = "image"    # 图片（存储 Base64 或 URL）
    CODE = "code"      # 代码片段


class Card(Base):
    """知识卡片模型"""

    __tablename__ = "cards"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    card_type = Column(Enum(CardType), nullable=False, default=CardType.NOTE)
    url = Column(String(500), nullable=True)  # 仅当 type=link 时使用
    is_pinned = Column(Boolean, default=False)
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # 关系
    user = relationship("User", back_populates="cards")
    tags = relationship("CardTag", back_populates="card", cascade="all, delete-orphan")
    source_links = relationship(
        "CardLink",
        foreign_keys="CardLink.source_card_id",
        back_populates="source_card",
        cascade="all, delete-orphan"
    )
    target_links = relationship(
        "CardLink",
        foreign_keys="CardLink.target_card_id",
        back_populates="target_card",
        cascade="all, delete-orphan"
    )
    kanban_items = relationship(
        "KanbanCard",
        back_populates="card",
        cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Card(id={self.id}, title='{self.title}', type='{self.card_type}')>"
