"""
搜索服务
"""
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from app.models.card import Card
from app.models.tag import Tag


class SearchService:
    """搜索服务类"""

    @staticmethod
    def search_cards(
        db: Session,
        user_id: int,
        keyword: str,
        skip: int = 0,
        limit: int = 20
    ) -> tuple[List[Dict], int]:
        """
        搜索卡片

        Args:
            db: 数据库会话
            user_id: 用户ID
            keyword: 搜索关键词
            skip: 跳过记录数
            limit: 返回记录数

        Returns:
            tuple[List[Dict], int]: 卡片列表和总数
        """
        search_pattern = f"%{keyword}%"

        # 构建搜索查询
        query = db.query(Card).filter(
            and_(
                Card.user_id == user_id,
                or_(
                    Card.title.like(search_pattern),
                    Card.content.like(search_pattern)
                )
            )
        )

        # 获取总数
        total = query.count()

        # 分页
        cards = query.offset(skip).limit(limit).all()

        # 转换为字典
        items = []
        for card in cards:
            items.append({
                "id": card.id,
                "title": card.title,
                "content": card.content,
                "card_type": card.card_type,
                "url": card.url,
                "is_pinned": card.is_pinned,
                "view_count": card.view_count,
                "created_at": card.created_at,
                "updated_at": card.updated_at
            })

        return items, total

    @staticmethod
    def search_tags(
        db: Session,
        user_id: int,
        keyword: str
    ) -> List[Dict]:
        """
        搜索标签

        Args:
            db: 数据库会话
            user_id: 用户ID
            keyword: 搜索关键词

        Returns:
            List[Dict]: 标签列表
        """
        search_pattern = f"%{keyword}%"

        tags = db.query(Tag).filter(
            and_(
                Tag.user_id == user_id,
                Tag.name.like(search_pattern)
            )
        ).all()

        # 转换为字典
        items = []
        for tag in tags:
            items.append({
                "id": tag.id,
                "name": tag.name,
                "color": tag.color,
                "parent_id": tag.parent_id
            })

        return items

    @staticmethod
    def global_search(
        db: Session,
        user_id: int,
        keyword: str,
        search_type: str = "all",
        skip: int = 0,
        limit: int = 20
    ) -> Dict:
        """
        全局搜索

        Args:
            db: 数据库会话
            user_id: 用户ID
            keyword: 搜索关键词
            search_type: 搜索类型（all/cards/tags）
            skip: 跳过记录数
            limit: 返回记录数

        Returns:
            Dict: 搜索结果
        """
        result = {}

        # 搜索卡片
        if search_type in ["all", "cards"]:
            cards, total = SearchService.search_cards(
                db, user_id, keyword, skip, limit
            )
            result["cards"] = {
                "items": cards,
                "total": total
            }

        # 搜索标签
        if search_type in ["all", "tags"]:
            tags = SearchService.search_tags(db, user_id, keyword)
            result["tags"] = {
                "items": tags,
                "total": len(tags)
            }

        # 计算总数
        total = 0
        if "cards" in result:
            total += result["cards"]["total"]
        if "tags" in result:
            total += result["tags"]["total"]
        result["total"] = total

        return result
