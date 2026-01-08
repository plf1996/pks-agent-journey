"""
看板相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.kanban import (
    KanbanColumnCreate,
    KanbanColumnUpdate,
    KanbanBoardResponse,
    MoveCardRequest,
    MoveCardResponse,
    BatchMoveRequest,
    BatchMoveResponse
)
from app.schemas.common import ApiResponse
from app.services.kanban_service import KanbanService

router = APIRouter()


@router.get("", response_model=ApiResponse[KanbanBoardResponse])
def get_kanban_board(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取看板配置"""
    # 初始化默认列（如果是第一次）
    KanbanService.init_default_columns(db, current_user.id)

    columns = KanbanService.get_kanban_board(db, current_user.id)

    return ApiResponse(
        code=0,
        message="success",
        data={"columns": columns}
    )


@router.post("/columns", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create_column(
    column_in: KanbanColumnCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建看板列"""
    try:
        column = KanbanService.create_column(db, current_user.id, column_in)
        return ApiResponse(
            code=0,
            message="创建成功",
            data=column
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.put("/columns/{column_id}", response_model=ApiResponse)
def update_column(
    column_id: int,
    column_in: KanbanColumnUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新看板列"""
    from app.models.kanban import KanbanColumn

    column = db.query(KanbanColumn).filter(
        KanbanColumn.id == column_id,
        KanbanColumn.user_id == current_user.id
    ).first()

    if not column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="列不存在"
        )

    try:
        updated_column = KanbanService.update_column(db, column, column_in)
        return ApiResponse(
            code=0,
            message="更新成功",
            data=updated_column
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.delete("/columns/{column_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_column(
    column_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除看板列"""
    from app.models.kanban import KanbanColumn

    column = db.query(KanbanColumn).filter(
        KanbanColumn.id == column_id,
        KanbanColumn.user_id == current_user.id
    ).first()

    if not column:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="列不存在"
        )

    KanbanService.delete_column(db, column)


@router.post("/cards/move", response_model=ApiResponse[MoveCardResponse])
def move_card(
    request: MoveCardRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """移动卡片到指定列的指定位置"""
    try:
        result = KanbanService.move_card(
            db,
            current_user.id,
            request.card_id,
            request.column_id,
            request.position
        )
        return ApiResponse(
            code=0,
            message="移动成功",
            data=result
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/cards/batch-move", response_model=ApiResponse[BatchMoveResponse])
def batch_move_cards(
    request: BatchMoveRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """批量移动卡片到指定列"""
    try:
        moved_count = KanbanService.batch_move_cards(
            db,
            current_user.id,
            request.card_ids,
            request.target_column_id
        )
        return ApiResponse(
            code=0,
            message="移动成功",
            data={"moved_count": moved_count}
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
