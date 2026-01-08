"""
标签相关数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class Tag(Base):
    """标签模型"""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(String(50), nullable=False)
    color = Column(String(7), default="#1976D2")  # 十六进制颜色码
    parent_id = Column(
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # 关系
    user = relationship("User", back_populates="tags")
    parent = relationship("Tag", remote_side=[id], back_populates="children")
    children = relationship("Tag", back_populates="parent", cascade="all, delete-orphan")
    card_tags = relationship("CardTag", back_populates="tag", cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('user_id', 'name', name='uq_tag_user_name'),
    )

    def __repr__(self) -> str:
        return f"<Tag(id={self.id}, name='{self.name}', color='{self.color}')>"


class CardTag(Base):
    """卡片标签关联模型（多对多关系）"""

    __tablename__ = "card_tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(
        Integer,
        ForeignKey("cards.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    tag_id = Column(
        Integer,
        ForeignKey("tags.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # 关系
    card = relationship("Card", back_populates="tags")
    tag = relationship("Tag", back_populates="card_tags")

    __table_args__ = (
        UniqueConstraint('card_id', 'tag_id', name='uq_card_tag'),
    )

    def __repr__(self) -> str:
        return f"<CardTag(card_id={self.card_id}, tag_id={self.tag_id})>"
