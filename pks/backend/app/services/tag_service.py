"""
标签服务
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from app.models.tag import Tag, CardTag
from app.models.card import Card
from app.schemas.tag import TagCreate, TagUpdate


class TagService:
    """标签服务类"""

    @staticmethod
    def get_tag_by_id(db: Session, tag_id: int, user_id: int) -> Optional[Tag]:
        """
        获取标签详情

        Args:
            db: 数据库会话
            tag_id: 标签ID
            user_id: 用户ID

        Returns:
            Optional[Tag]: 标签对象
        """
        return db.query(Tag).filter(
            and_(Tag.id == tag_id, Tag.user_id == user_id)
        ).first()

    @staticmethod
    def get_tags(
        db: Session,
        user_id: int,
        parent_id: Optional[int] = None
    ) -> List[Tag]:
        """
        获取标签列表

        Args:
            db: 数据库会话
            user_id: 用户ID
            parent_id: 父标签ID（None表示获取根标签）

        Returns:
            List[Tag]: 标签列表
        """
        query = db.query(Tag).filter(Tag.user_id == user_id)

        # 处理parent_id
        if parent_id is None:
            query = query.filter(Tag.parent_id.is_(None))
        else:
            query = query.filter(Tag.parent_id == parent_id)

        return query.order_by(Tag.name).all()

    @staticmethod
    def create_tag(db: Session, user_id: int, tag_in: TagCreate) -> Tag:
        """
        创建标签

        Args:
            db: 数据库会话
            user_id: 用户ID
            tag_in: 标签创建数据

        Returns:
            Tag: 创建的标签对象

        Raises:
            ValueError: 如果标签名称已存在
        """
        # 检查标签名称是否已存在
        existing = db.query(Tag).filter(
            and_(
                Tag.user_id == user_id,
                Tag.name == tag_in.name
            )
        ).first()

        if existing:
            raise ValueError("标签名称已存在")

        # 验证父标签是否存在
        if tag_in.parent_id:
            parent = TagService.get_tag_by_id(db, tag_in.parent_id, user_id)
            if not parent:
                raise ValueError("父标签不存在")

        # 创建标签
        db_tag = Tag(
            user_id=user_id,
            name=tag_in.name,
            color=tag_in.color,
            parent_id=tag_in.parent_id
        )
        db.add(db_tag)
        db.commit()
        db.refresh(db_tag)
        return db_tag

    @staticmethod
    def update_tag(db: Session, tag: Tag, tag_in: TagUpdate) -> Tag:
        """
        更新标签

        Args:
            db: 数据库会话
            tag: 标签对象
            tag_in: 更新数据

        Returns:
            Tag: 更新后的标签对象

        Raises:
            ValueError: 如果标签名称已存在
        """
        # 更新名称
        if tag_in.name is not None:
            # 检查名称是否已被其他标签使用
            existing = db.query(Tag).filter(
                and_(
                    Tag.user_id == tag.user_id,
                    Tag.name == tag_in.name,
                    Tag.id != tag.id
                )
            ).first()

            if existing:
                raise ValueError("标签名称已存在")

            tag.name = tag_in.name

        # 更新颜色
        if tag_in.color is not None:
            tag.color = tag_in.color

        db.commit()
        db.refresh(tag)
        return tag

    @staticmethod
    def delete_tag(db: Session, tag: Tag) -> None:
        """
        删除标签（级联删除子标签和关联）

        Args:
            db: 数据库会话
            tag: 标签对象
        """
        db.delete(tag)
        db.commit()

    @staticmethod
    def get_tag_with_children(db: Session, tag_id: int, user_id: int) -> Optional[dict]:
        """
        获取标签详情（包含子标签和关联的卡片）

        Args:
            db: 数据库会话
            tag_id: 标签ID
            user_id: 用户ID

        Returns:
            Optional[dict]: 标签详情字典
        """
        tag = TagService.get_tag_by_id(db, tag_id, user_id)
        if not tag:
            return None

        # 获取子标签
        children = db.query(Tag).filter(Tag.parent_id == tag_id).all()

        # 获取关联的卡片
        card_tags = db.query(CardTag).filter(CardTag.tag_id == tag_id).all()
        cards = []
        for ct in card_tags:
            card = db.query(Card).filter(Card.id == ct.card_id).first()
            if card:
                cards.append({
                    "id": card.id,
                    "title": card.title
                })

        return {
            "id": tag.id,
            "name": tag.name,
            "color": tag.color,
            "parent_id": tag.parent_id,
            "children": [
                {
                    "id": child.id,
                    "name": child.name,
                    "color": child.color,
                    "parent_id": child.parent_id
                }
                for child in children
            ],
            "cards": cards,
            "created_at": tag.created_at
        }

    @staticmethod
    def get_tag_stats(db: Session, user_id: int) -> List[dict]:
        """
        获取标签统计信息（按使用频率排序）

        Args:
            db: 数据库会话
            user_id: 用户ID

        Returns:
            List[dict]: 标签统计列表
        """
        # 统计每个标签的卡片数量
        stats = db.query(
            Tag.id,
            Tag.name,
            Tag.color,
            func.count(CardTag.id).label('cards_count')
        ).outerjoin(
            CardTag, Tag.id == CardTag.tag_id
        ).filter(
            Tag.user_id == user_id
        ).group_by(
            Tag.id, Tag.name, Tag.color
        ).order_by(
            desc('cards_count')
        ).all()

        return [
            {
                "id": stat.id,
                "name": stat.name,
                "color": stat.color,
                "cards_count": stat.cards_count
            }
            for stat in stats
        ]
