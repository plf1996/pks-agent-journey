"""
卡片服务
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_, desc, func
from app.models.card import Card, CardType
from app.models.tag import CardTag, Tag
from app.models.link import CardLink, LinkType
from app.schemas.card import CardCreate, CardUpdate


class CardService:
    """卡片服务类"""

    @staticmethod
    def get_card_by_id(db: Session, card_id: int, user_id: int) -> Optional[Card]:
        """
        获取卡片详情

        Args:
            db: 数据库会话
            card_id: 卡片ID
            user_id: 用户ID

        Returns:
            Optional[Card]: 卡片对象
        """
        return db.query(Card).filter(
            and_(Card.id == card_id, Card.user_id == user_id)
        ).first()

    @staticmethod
    def get_cards(
        db: Session,
        user_id: int,
        skip: int = 0,
        limit: int = 20,
        card_type: Optional[CardType] = None,
        tag_id: Optional[int] = None,
        is_pinned: Optional[bool] = None,
        search: Optional[str] = None,
        sort_by: str = "created_at",
        order: str = "desc"
    ) -> tuple[List[Card], int]:
        """
        获取卡片列表

        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过记录数
            limit: 返回记录数
            card_type: 卡片类型筛选
            tag_id: 标签筛选
            is_pinned: 是否置顶
            search: 搜索关键词
            sort_by: 排序字段
            order: 排序方向

        Returns:
            tuple[List[Card], int]: 卡片列表和总数
        """
        # 构建查询
        query = db.query(Card).filter(Card.user_id == user_id)

        # 卡片类型筛选
        if card_type:
            query = query.filter(Card.card_type == card_type)

        # 标签筛选
        if tag_id:
            query = query.join(CardTag).filter(CardTag.tag_id == tag_id)

        # 置顶筛选
        if is_pinned is not None:
            query = query.filter(Card.is_pinned == is_pinned)

        # 搜索
        if search:
            search_pattern = f"%{search}%"
            query = query.filter(
                or_(
                    Card.title.like(search_pattern),
                    Card.content.like(search_pattern)
                )
            )

        # 获取总数
        total = query.count()

        # 排序
        sort_column = getattr(Card, sort_by, Card.created_at)
        if order == "desc":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)

        # 分页
        cards = query.offset(skip).limit(limit).all()

        # 加载标签关系
        for card in cards:
            db.refresh(card, attribute_names=['tags'])

        return cards, total

    @staticmethod
    def create_card(db: Session, user_id: int, card_in: CardCreate) -> Card:
        """
        创建卡片

        Args:
            db: 数据库会话
            user_id: 用户ID
            card_in: 卡片创建数据

        Returns:
            Card: 创建的卡片对象
        """
        # 创建卡片
        db_card = Card(
            user_id=user_id,
            title=card_in.title,
            content=card_in.content,
            card_type=card_in.card_type,
            url=card_in.url
        )
        db.add(db_card)
        db.flush()  # 获取card_id

        # 添加标签关联
        if card_in.tag_ids:
            for tag_id in card_in.tag_ids:
                # 验证标签是否存在且属于当前用户
                tag = db.query(Tag).filter(
                    and_(Tag.id == tag_id, Tag.user_id == user_id)
                ).first()
                if tag:
                    card_tag = CardTag(card_id=db_card.id, tag_id=tag_id)
                    db.add(card_tag)

        # 创建双向链接
        if card_in.link_ids:
            for target_id in card_in.link_ids:
                # 验证目标卡片是否存在且属于当前用户
                target_card = CardService.get_card_by_id(db, target_id, user_id)
                if target_card and target_id != db_card.id:
                    # 创建正向链接
                    link1 = CardLink(
                        source_card_id=db_card.id,
                        target_card_id=target_id,
                        link_type=LinkType.REFERENCE
                    )
                    # 创建反向链接
                    link2 = CardLink(
                        source_card_id=target_id,
                        target_card_id=db_card.id,
                        link_type=LinkType.REFERENCE
                    )
                    db.add(link1)
                    db.add(link2)

        db.commit()
        db.refresh(db_card)
        return db_card

    @staticmethod
    def update_card(
        db: Session,
        card: Card,
        card_in: CardUpdate
    ) -> Card:
        """
        更新卡片

        Args:
            db: 数据库会话
            card: 卡片对象
            card_in: 更新数据

        Returns:
            Card: 更新后的卡片对象
        """
        # 更新字段
        update_data = card_in.model_dump(exclude_unset=True)

        # 分离处理标签
        tag_ids = update_data.pop('tag_ids', None)

        for field, value in update_data.items():
            setattr(card, field, value)

        # 更新标签关联
        if tag_ids is not None:
            # 删除旧的标签关联
            db.query(CardTag).filter(CardTag.card_id == card.id).delete()

            # 添加新的标签关联
            for tag_id in tag_ids:
                # 验证标签是否存在且属于当前用户
                tag = db.query(Tag).filter(
                    and_(Tag.id == tag_id, Tag.user_id == card.user_id)
                ).first()
                if tag:
                    card_tag = CardTag(card_id=card.id, tag_id=tag_id)
                    db.add(card_tag)

        db.commit()
        db.refresh(card)
        return card

    @staticmethod
    def delete_card(db: Session, card: Card) -> None:
        """
        删除卡片

        Args:
            db: 数据库会话
            card: 卡片对象
        """
        db.delete(card)
        db.commit()

    @staticmethod
    def batch_delete_cards(db: Session, card_ids: List[int], user_id: int) -> int:
        """
        批量删除卡片

        Args:
            db: 数据库会话
            card_ids: 卡片ID列表
            user_id: 用户ID

        Returns:
            int: 删除的数量
        """
        # 删除属于当前用户的卡片
        count = db.query(Card).filter(
            and_(
                Card.id.in_(card_ids),
                Card.user_id == user_id
            )
        ).delete(synchronize_session=False)
        db.commit()
        return count

    @staticmethod
    def increment_view_count(db: Session, card: Card) -> None:
        """
        增加卡片浏览次数

        Args:
            db: 数据库会话
            card: 卡片对象
        """
        card.view_count += 1
        db.commit()

    @staticmethod
    def get_card_links(db: Session, card: Card) -> Dict[str, List[Dict]]:
        """
        获取卡片的所有链接

        Args:
            db: 数据库会话
            card: 卡片对象

        Returns:
            Dict: 包含出链和入链的字典
        """
        # 正向链接（我链接到的卡片）
        outgoing_links = db.query(CardLink).filter(
            CardLink.source_card_id == card.id
        ).all()

        # 反向链接（链接到我的卡片）
        incoming_links = db.query(CardLink).filter(
            CardLink.target_card_id == card.id
        ).all()

        # 构建响应数据
        outgoing = []
        for link in outgoing_links:
            target_card = db.query(Card).filter(Card.id == link.target_card_id).first()
            if target_card:
                outgoing.append({
                    "id": target_card.id,
                    "title": target_card.title,
                    "link_type": link.link_type,
                    "created_at": link.created_at
                })

        incoming = []
        for link in incoming_links:
            source_card = db.query(Card).filter(Card.id == link.source_card_id).first()
            if source_card:
                incoming.append({
                    "id": source_card.id,
                    "title": source_card.title,
                    "link_type": link.link_type,
                    "created_at": link.created_at
                })

        return {
            "outgoing": outgoing,
            "incoming": incoming,
            "total": len(outgoing) + len(incoming)
        }

    @staticmethod
    def create_card_link(
        db: Session,
        source_card: Card,
        target_card_id: int,
        link_type: LinkType = LinkType.REFERENCE
    ) -> Dict[str, Any]:
        """
        创建卡片链接

        Args:
            db: 数据库会话
            source_card: 源卡片
            target_card_id: 目标卡片ID
            link_type: 链接类型

        Returns:
            Dict: 链接信息
        """
        # 验证目标卡片
        target_card = db.query(Card).filter(
            and_(
                Card.id == target_card_id,
                Card.user_id == source_card.user_id
            )
        ).first()

        if not target_card:
            raise ValueError("目标卡片不存在")

        if target_card_id == source_card.id:
            raise ValueError("不能链接到自己")

        # 检查链接是否已存在
        existing = db.query(CardLink).filter(
            and_(
                CardLink.source_card_id == source_card.id,
                CardLink.target_card_id == target_card_id
            )
        ).first()

        if existing:
            raise ValueError("链接已存在")

        # 创建双向链接
        link1 = CardLink(
            source_card_id=source_card.id,
            target_card_id=target_card_id,
            link_type=link_type
        )
        link2 = CardLink(
            source_card_id=target_card_id,
            target_card_id=source_card.id,
            link_type=link_type
        )
        db.add(link1)
        db.add(link2)
        db.commit()

        return {
            "source_card": {"id": source_card.id, "title": source_card.title},
            "target_card": {"id": target_card.id, "title": target_card.title},
            "link_type": link_type
        }

    @staticmethod
    def delete_card_link(db: Session, source_card: Card, target_card_id: int) -> None:
        """
        删除卡片链接（双向）

        Args:
            db: 数据库会话
            source_card: 源卡片
            target_card_id: 目标卡片ID
        """
        # 删除正向链接
        db.query(CardLink).filter(
            and_(
                CardLink.source_card_id == source_card.id,
                CardLink.target_card_id == target_card_id
            )
        ).delete()

        # 删除反向链接
        db.query(CardLink).filter(
            and_(
                CardLink.source_card_id == target_card_id,
                CardLink.target_card_id == source_card.id
            )
        ).delete()

        db.commit()

    @staticmethod
    def batch_tag_cards(
        db: Session,
        card_ids: List[int],
        tag_ids: List[int],
        user_id: int
    ) -> int:
        """
        批量为卡片打标签

        Args:
            db: 数据库会话
            card_ids: 卡片ID列表
            tag_ids: 标签ID列表
            user_id: 用户ID

        Returns:
            int: 影响的卡片数量
        """
        affected_count = 0

        for card_id in card_ids:
            # 验证卡片是否存在
            card = CardService.get_card_by_id(db, card_id, user_id)
            if not card:
                continue

            # 为每个标签创建关联
            for tag_id in tag_ids:
                # 检查关联是否已存在
                existing = db.query(CardTag).filter(
                    and_(
                        CardTag.card_id == card_id,
                        CardTag.tag_id == tag_id
                    )
                ).first()

                if not existing:
                    # 验证标签是否存在且属于当前用户
                    tag = db.query(Tag).filter(
                        and_(Tag.id == tag_id, Tag.user_id == user_id)
                    ).first()
                    if tag:
                        card_tag = CardTag(card_id=card_id, tag_id=tag_id)
                        db.add(card_tag)
                        affected_count += 1

        db.commit()
        return affected_count
