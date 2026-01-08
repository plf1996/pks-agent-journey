"""
看板服务
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from app.models.kanban import KanbanColumn, KanbanCard
from app.models.card import Card
from app.schemas.kanban import KanbanColumnCreate, KanbanColumnUpdate


class KanbanService:
    """看板服务类"""

    @staticmethod
    def init_default_columns(db: Session, user_id: int) -> None:
        """
        初始化默认看板列

        Args:
            db: 数据库会话
            user_id: 用户ID
        """
        # 检查是否已有看板列
        existing = db.query(KanbanColumn).filter(
            KanbanColumn.user_id == user_id
        ).first()

        if existing:
            return

        # 创建默认三列
        default_columns = [
            {"name": "待处理", "position": 0},
            {"name": "进行中", "position": 1},
            {"name": "已完成", "position": 2}
        ]

        for col in default_columns:
            db_col = KanbanColumn(
                user_id=user_id,
                name=col["name"],
                position=col["position"]
            )
            db.add(db_col)

        db.commit()

    @staticmethod
    def get_kanban_board(db: Session, user_id: int) -> List[dict]:
        """
        获取看板配置（包含所有列和卡片）

        Args:
            db: 数据库会话
            user_id: 用户ID

        Returns:
            List[dict]: 看板列列表（包含卡片）
        """
        # 获取所有列
        columns = db.query(KanbanColumn).filter(
            KanbanColumn.user_id == user_id
        ).order_by(KanbanColumn.position).all()

        result = []
        for column in columns:
            # 获取列中的卡片
            kanban_cards = db.query(KanbanCard).filter(
                KanbanCard.column_id == column.id
            ).order_by(KanbanCard.position).all()

            cards_data = []
            for kc in kanban_cards:
                card = db.query(Card).filter(Card.id == kc.card_id).first()
                if card:
                    cards_data.append({
                        "id": card.id,
                        "title": card.title,
                        "position": kc.position
                    })

            result.append({
                "id": column.id,
                "name": column.name,
                "position": column.position,
                "user_id": column.user_id,
                "created_at": column.created_at,
                "updated_at": column.updated_at,
                "cards_count": len(cards_data),
                "cards": cards_data
            })

        return result

    @staticmethod
    def create_column(
        db: Session,
        user_id: int,
        column_in: KanbanColumnCreate
    ) -> KanbanColumn:
        """
        创建看板列

        Args:
            db: 数据库会话
            user_id: 用户ID
            column_in: 列创建数据

        Returns:
            KanbanColumn: 创建的列对象
        """
        # 检查位置是否已被占用
        existing = db.query(KanbanColumn).filter(
            and_(
                KanbanColumn.user_id == user_id,
                KanbanColumn.position == column_in.position
            )
        ).first()

        if existing:
            raise ValueError("该位置已被占用")

        db_column = KanbanColumn(
            user_id=user_id,
            name=column_in.name,
            position=column_in.position
        )
        db.add(db_column)
        db.commit()
        db.refresh(db_column)
        return db_column

    @staticmethod
    def update_column(
        db: Session,
        column: KanbanColumn,
        column_in: KanbanColumnUpdate
    ) -> KanbanColumn:
        """
        更新看板列

        Args:
            db: 数据库会话
            column: 列对象
            column_in: 更新数据

        Returns:
            KanbanColumn: 更新后的列对象
        """
        if column_in.name is not None:
            column.name = column_in.name

        if column_in.position is not None:
            # 检查位置是否已被其他列占用
            existing = db.query(KanbanColumn).filter(
                and_(
                    KanbanColumn.user_id == column.user_id,
                    KanbanColumn.position == column_in.position,
                    KanbanColumn.id != column.id
                )
            ).first()

            if existing:
                raise ValueError("该位置已被占用")

            column.position = column_in.position

        db.commit()
        db.refresh(column)
        return column

    @staticmethod
    def delete_column(db: Session, column: KanbanColumn) -> None:
        """
        删除看板列（级联删除列中的卡片）

        Args:
            db: 数据库会话
            column: 列对象
        """
        db.delete(column)
        db.commit()

    @staticmethod
    def move_card(
        db: Session,
        user_id: int,
        card_id: int,
        column_id: int,
        position: int
    ) -> dict:
        """
        移动卡片到指定列的指定位置

        Args:
            db: 数据库会话
            user_id: 用户ID
            card_id: 卡片ID
            column_id: 目标列ID
            position: 位置

        Returns:
            dict: 移动结果
        """
        # 验证卡片是否存在
        card = db.query(Card).filter(
            and_(Card.id == card_id, Card.user_id == user_id)
        ).first()

        if not card:
            raise ValueError("卡片不存在")

        # 验证列是否存在
        column = db.query(KanbanColumn).filter(
            and_(KanbanColumn.id == column_id, KanbanColumn.user_id == user_id)
        ).first()

        if not column:
            raise ValueError("列不存在")

        # 检查位置是否已被占用
        existing = db.query(KanbanCard).filter(
            and_(
                KanbanCard.column_id == column_id,
                KanbanCard.position == position
            )
        ).first()

        # 如果卡片已在看板中，删除旧位置
        old_kanban_card = db.query(KanbanCard).filter(
            KanbanCard.card_id == card_id
        ).first()

        if old_kanban_card:
            # 删除旧位置
            db.delete(old_kanban_card)

            # 如果移动到同一列且位置更大，需要调整位置
            if old_kanban_card.column_id == column_id:
                if old_kanban_card.position < position:
                    position -= 1

        # 如果目标位置已被占用，需要移动其他卡片
        if existing:
            # 将该位置及之后的卡片后移
            db.query(KanbanCard).filter(
                and_(
                    KanbanCard.column_id == column_id,
                    KanbanCard.position >= position
                )
            ).update({
                "position": KanbanCard.position + 1
            })

        # 创建新的看板卡片关联
        kanban_card = KanbanCard(
            card_id=card_id,
            column_id=column_id,
            position=position
        )
        db.add(kanban_card)

        db.commit()

        return {
            "card_id": card_id,
            "column_id": column_id,
            "position": position
        }

    @staticmethod
    def batch_move_cards(
        db: Session,
        user_id: int,
        card_ids: List[int],
        target_column_id: int
    ) -> int:
        """
        批量移动卡片到指定列

        Args:
            db: 数据库会话
            user_id: 用户ID
            card_ids: 卡片ID列表
            target_column_id: 目标列ID

        Returns:
            int: 移动的卡片数量
        """
        # 验证目标列是否存在
        target_column = db.query(KanbanColumn).filter(
            and_(
                KanbanColumn.id == target_column_id,
                KanbanColumn.user_id == user_id
            )
        ).first()

        if not target_column:
            raise ValueError("目标列不存在")

        moved_count = 0

        for card_id in card_ids:
            # 验证卡片是否存在
            card = db.query(Card).filter(
                and_(Card.id == card_id, Card.user_id == user_id)
            ).first()

            if not card:
                continue

            # 获取目标列的下一个位置
            max_position = db.query(func.max(KanbanCard.position)).filter(
                KanbanCard.column_id == target_column_id
            ).scalar() or -1

            # 检查卡片是否已在看板中
            existing = db.query(KanbanCard).filter(
                KanbanCard.card_id == card_id
            ).first()

            if existing:
                # 更新到新列
                existing.column_id = target_column_id
                existing.position = max_position + 1
            else:
                # 创建新关联
                kanban_card = KanbanCard(
                    card_id=card_id,
                    column_id=target_column_id,
                    position=max_position + 1
                )
                db.add(kanban_card)

            moved_count += 1

        db.commit()
        return moved_count
