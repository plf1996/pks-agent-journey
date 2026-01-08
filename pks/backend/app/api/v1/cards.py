"""
卡片相关API路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.card import CardType
from app.schemas.card import (
    CardCreate,
    CardUpdate,
    CardResponse,
    CardDetailResponse,
    CardListResponse,
    BatchDeleteRequest,
    BatchDeleteResponse,
    BatchTagRequest,
    BatchTagResponse
)
from app.schemas.common import ApiResponse, PaginatedResponse
from app.services.card_service import CardService

router = APIRouter()


@router.post("", response_model=ApiResponse[CardResponse], status_code=status.HTTP_201_CREATED)
def create_card(
    card_in: CardCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建卡片"""
    try:
        card = CardService.create_card(db, current_user.id, card_in)

        # 构建标签数据
        tags_data = []
        for ct in card.tags:
            tags_data.append({
                "id": ct.tag.id,
                "name": ct.tag.name,
                "color": ct.tag.color
            })

        # 构建响应数据
        card_data = {
            "id": card.id,
            "title": card.title,
            "content": card.content,
            "card_type": card.card_type,
            "url": card.url,
            "user_id": card.user_id,
            "is_pinned": card.is_pinned,
            "view_count": card.view_count,
            "created_at": card.created_at,
            "updated_at": card.updated_at,
            "tags": tags_data
        }

        return ApiResponse(
            code=0,
            message="创建成功",
            data=card_data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("", response_model=ApiResponse[PaginatedResponse])
def get_cards(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    card_type: Optional[str] = Query(None, description="卡片类型"),
    tag_id: Optional[int] = Query(None, description="标签ID"),
    is_pinned: Optional[str] = Query(None, description="是否置顶"),
    search: Optional[str] = Query(None, description="搜索关键词"),
    sort_by: str = Query("created_at", description="排序字段"),
    order: str = Query("desc", regex="^(asc|desc)$", description="排序方向"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取卡片列表"""
    skip = (page - 1) * page_size

    # 处理 card_type 参数（空字符串转为 None）
    parsed_card_type = None
    if card_type and card_type.strip():
        try:
            parsed_card_type = CardType(card_type)
        except ValueError:
            pass

    # 处理 is_pinned 参数（字符串转为布尔值）
    parsed_is_pinned = None
    if is_pinned is not None and is_pinned.strip():
        parsed_is_pinned = is_pinned.lower() in ('true', '1', 'yes')

    cards, total = CardService.get_cards(
        db,
        current_user.id,
        skip=skip,
        limit=page_size,
        card_type=parsed_card_type,
        tag_id=tag_id,
        is_pinned=parsed_is_pinned,
        search=search,
        sort_by=sort_by,
        order=order
    )

    total_pages = (total + page_size - 1) // page_size

    # 转换 Card 对象为字典
    items_data = []
    for card in cards:
        items_data.append({
            "id": card.id,
            "title": card.title,
            "content": card.content,
            "card_type": card.card_type,
            "user_id": card.user_id,
            "is_pinned": card.is_pinned,
            "view_count": card.view_count,
            "created_at": card.created_at,
            "updated_at": card.updated_at
        })

    return ApiResponse(
        code=0,
        message="success",
        data=PaginatedResponse(
            items=items_data,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
    )


@router.get("/{card_id}", response_model=ApiResponse[CardDetailResponse])
def get_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取卡片详情"""
    card = CardService.get_card_by_id(db, card_id, current_user.id)

    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="卡片不存在"
        )

    # 增加浏览次数
    CardService.increment_view_count(db, card)

    # 获取链接信息
    links = CardService.get_card_links(db, card)

    # 转换 Card 对象为字典
    card_data = {
        "id": card.id,
        "title": card.title,
        "content": card.content,
        "card_type": card.card_type,
        "user_id": card.user_id,
        "is_pinned": card.is_pinned,
        "view_count": card.view_count,
        "created_at": card.created_at,
        "updated_at": card.updated_at
    }

    return ApiResponse(
        code=0,
        message="success",
        data={
            **card_data,
            "links": links
        }
    )


@router.put("/{card_id}", response_model=ApiResponse[CardResponse])
def update_card(
    card_id: int,
    card_in: CardUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新卡片"""
    card = CardService.get_card_by_id(db, card_id, current_user.id)

    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="卡片不存在"
        )

    try:
        updated_card = CardService.update_card(db, card, card_in)

        # 构建标签数据
        tags_data = []
        for ct in updated_card.tags:
            tags_data.append({
                "id": ct.tag.id,
                "name": ct.tag.name,
                "color": ct.tag.color
            })

        # 构建响应数据
        card_data = {
            "id": updated_card.id,
            "title": updated_card.title,
            "content": updated_card.content,
            "card_type": updated_card.card_type,
            "url": updated_card.url,
            "user_id": updated_card.user_id,
            "is_pinned": updated_card.is_pinned,
            "view_count": updated_card.view_count,
            "created_at": updated_card.created_at,
            "updated_at": updated_card.updated_at,
            "tags": tags_data
        }

        return ApiResponse(
            code=0,
            message="更新成功",
            data=card_data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(
    card_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除卡片"""
    card = CardService.get_card_by_id(db, card_id, current_user.id)

    if not card:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="卡片不存在"
        )

    CardService.delete_card(db, card)


@router.post("/batch-delete", response_model=ApiResponse[BatchDeleteResponse])
def batch_delete_cards(
    request: BatchDeleteRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """批量删除卡片"""
    deleted_count = CardService.batch_delete_cards(
        db,
        request.card_ids,
        current_user.id
    )

    return ApiResponse(
        code=0,
        message="删除成功",
        data={"deleted_count": deleted_count}
    )
