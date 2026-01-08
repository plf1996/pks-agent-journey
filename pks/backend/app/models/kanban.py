"""
看板相关数据模型
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.base import Base


class KanbanColumn(Base):
    """看板列模型"""

    __tablename__ = "kanban_columns"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    name = Column(String(50), nullable=False)
    position = Column(Integer, nullable=False)  # 排序位置
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # 关系
    user = relationship("User", back_populates="kanban_columns")
    kanban_cards = relationship(
        "KanbanCard",
        back_populates="column",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'position', name='uq_kanban_column_user_position'),
    )

    def __repr__(self) -> str:
        return f"<KanbanColumn(id={self.id}, name='{self.name}', position={self.position})>"


class KanbanCard(Base):
    """看板卡片关联模型"""

    __tablename__ = "kanban_cards"

    id = Column(Integer, primary_key=True, autoincrement=True)
    card_id = Column(
        Integer,
        ForeignKey("cards.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    column_id = Column(
        Integer,
        ForeignKey("kanban_columns.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    position = Column(Integer, nullable=False)  # 在列中的排序位置
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    # 关系
    card = relationship("Card", back_populates="kanban_items")
    column = relationship("KanbanColumn", back_populates="kanban_cards")

    __table_args__ = (
        UniqueConstraint('column_id', 'position', name='uq_kanban_card_column_position'),
    )

    def __repr__(self) -> str:
        return f"<KanbanCard(card_id={self.card_id}, column_id={self.column_id}, position={self.position})>"
