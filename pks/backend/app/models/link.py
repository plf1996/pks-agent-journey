"""
卡片链接数据模型
"""
import enum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class LinkType(str, enum.Enum):
    """链接类型枚举"""
    REFERENCE = "reference"  # 普通引用
    RELATED = "related"      # 相关推荐
    PARENT = "parent"        # 父子关系


class CardLink(Base):
    """卡片链接模型"""

    __tablename__ = "card_links"

    id = Column(Integer, primary_key=True, autoincrement=True)
    source_card_id = Column(
        Integer,
        ForeignKey("cards.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    target_card_id = Column(
        Integer,
        ForeignKey("cards.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    link_type = Column(String(20), default=LinkType.REFERENCE)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    source_card = relationship(
        "Card",
        foreign_keys=[source_card_id],
        back_populates="source_links"
    )
    target_card = relationship(
        "Card",
        foreign_keys=[target_card_id],
        back_populates="target_links"
    )

    __table_args__ = (
        UniqueConstraint('source_card_id', 'target_card_id', name='uq_card_link'),
    )

    def __repr__(self) -> str:
        return f"<CardLink(source={self.source_card_id}, target={self.target_card_id}, type='{self.link_type}')>"
