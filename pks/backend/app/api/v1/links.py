"""
卡片链接相关API路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.link import LinkType
from app.schemas.card import CardLinkInfo
from app.schemas.common import ApiResponse
from app.services.card_service import CardService

router = APIRouter()


@router.post("/{card_id}/links", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create_card_link(
    card_id: int,
    target_card_id: int,
    link_type: LinkType = LinkType.REFERENCE,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建卡片链接（双向）"""
    source_card = CardService.get_card_by_id(db, card_id, current_user.id)

    if not source_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="源卡片不存在"
        )

    try:
        link_info = CardService.create_card_link(
            db,
            source_card,
            target_card_id,
            link_type
        )
        return ApiResponse(
            code=0,
            message="创建成功",
            data=link_info
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{card_id}/links", response_model=ApiResponse)
def get_card_links(
    card_id: int,
    link_type: Optional[LinkType] = Query(None, description="链接类型"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取卡片的所有链接"""
    card = CardService.get_card_by_id(db, card_id, current_user.id)

    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="卡片不存在"
        )

    links = CardService.get_card_links(db, card)

    # 如果指定了链接类型，进行过滤
    if link_type:
        links["outgoing"] = [
            link for link in links["outgoing"]
            if link["link_type"] == link_type
        ]
        links["incoming"] = [
            link for link in links["incoming"]
            if link["link_type"] == link_type
        ]
        links["total"] = len(links["outgoing"]) + len(links["incoming"])

    return ApiResponse(
        code=0,
        message="success",
        data=links
    )


@router.delete("/{card_id}/links/{target_card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card_link(
    card_id: int,
    target_card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除卡片链接（双向）"""
    source_card = CardService.get_card_by_id(db, card_id, current_user.id)

    if not source_card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="源卡片不存在"
        )

    CardService.delete_card_link(db, source_card, target_card_id)
