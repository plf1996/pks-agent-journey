"""
标签相关API路由
"""
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.tag import (
    TagCreate,
    TagUpdate,
    TagResponse,
    TagDetailResponse,
    TagWithCount
)
from app.schemas.common import ApiResponse
from app.services.tag_service import TagService

router = APIRouter()


@router.post("", response_model=ApiResponse[TagResponse], status_code=status.HTTP_201_CREATED)
def create_tag(
    tag_in: TagCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建标签"""
    try:
        tag = TagService.create_tag(db, current_user.id, tag_in)
        return ApiResponse(
            code=0,
            message="创建成功",
            data=tag
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get("", response_model=ApiResponse[List[TagWithCount]])
def get_tags(
    parent_id: Optional[int] = Query(None, description="父标签ID"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取标签列表"""
    tags = TagService.get_tags(db, current_user.id, parent_id)

    # 为每个标签添加统计信息
    result = []
    for tag in tags:
        children_count = len(tag.children)
        cards_count = len(tag.card_tags)
        result.append({
            "id": tag.id,
            "name": tag.name,
            "color": tag.color,
            "parent_id": tag.parent_id,
            "user_id": tag.user_id,
            "created_at": tag.created_at,
            "updated_at": tag.updated_at,
            "children_count": children_count,
            "cards_count": cards_count
        })

    return ApiResponse(
        code=0,
        message="success",
        data=result
    )


@router.get("/{tag_id}", response_model=ApiResponse[TagDetailResponse])
def get_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取标签详情"""
    tag_detail = TagService.get_tag_with_children(db, tag_id, current_user.id)

    if not tag_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在"
        )

    return ApiResponse(
        code=0,
        message="success",
        data=tag_detail
    )


@router.put("/{tag_id}", response_model=ApiResponse[TagResponse])
def update_tag(
    tag_id: int,
    tag_in: TagUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新标签"""
    tag = TagService.get_tag_by_id(db, tag_id, current_user.id)

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在"
        )

    try:
        updated_tag = TagService.update_tag(db, tag, tag_in)
        return ApiResponse(
            code=0,
            message="更新成功",
            data=updated_tag
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/{tag_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tag(
    tag_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除标签"""
    tag = TagService.get_tag_by_id(db, tag_id, current_user.id)

    if not tag:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="标签不存在"
        )

    TagService.delete_tag(db, tag)
