"""
搜索相关API路由
"""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.search import SearchQuery, SearchResponse
from app.schemas.common import ApiResponse
from app.services.search_service import SearchService

router = APIRouter()


@router.get("", response_model=ApiResponse[SearchResponse])
def global_search(
    q: str = Query(..., min_length=1, description="搜索关键词"),
    type: str = Query("all", regex="^(all|cards|tags)$", description="搜索类型"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """全局搜索"""
    skip = (page - 1) * page_size

    result = SearchService.global_search(
        db,
        current_user.id,
        q,
        search_type=type,
        skip=skip,
        limit=page_size
    )

    return ApiResponse(
        code=0,
        message="success",
        data=result
    )
