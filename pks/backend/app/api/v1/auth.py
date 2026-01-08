"""
认证相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserWithToken,
    LoginRequest,
    Token
)
from app.services.auth_service import AuthService
from app.schemas.common import ApiResponse

router = APIRouter()


@router.post("/register", response_model=ApiResponse[UserWithToken], status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    用户注册

    创建新用户并返回访问令牌
    """
    try:
        # 创建用户
        user = AuthService.create_user(db, user_in)

        # 生成Token
        tokens = AuthService.create_user_tokens(user)

        # 构建响应
        from app.schemas.user import UserResponse
        user_data = UserResponse.model_validate(user).model_dump()
        response_data = {
            **user_data,
            **tokens
        }

        return ApiResponse(
            code=0,
            message="注册成功",
            data=response_data
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=ApiResponse[UserWithToken])
def login(user_credentials: LoginRequest, db: Session = Depends(get_db)):
    """
    用户登录

    支持用户名或邮箱登录
    """
    # 验证用户
    user = AuthService.authenticate_user(
        db,
        username=user_credentials.username,
        email=user_credentials.email,
        password=user_credentials.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 生成Token
    tokens = AuthService.create_user_tokens(user)

    # 构建响应
    from app.schemas.user import UserResponse
    user_data = UserResponse.model_validate(user).model_dump()
    response_data = {
        **user_data,
        **tokens
    }

    return ApiResponse(
        code=0,
        message="登录成功",
        data=response_data
    )


@router.get("/me", response_model=ApiResponse[UserResponse])
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """
    获取当前用户信息

    需要认证
    """
    return ApiResponse(
        code=0,
        message="success",
        data=current_user
    )
