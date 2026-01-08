"""
API依赖注入

提供常用的依赖项,如获取当前用户、数据库会话等
"""
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.core.security import verify_token
from app.models.user import User
from app.services.auth_service import AuthService

# OAuth2 密码模式
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    获取当前登录用户

    Args:
        token: JWT Token
        db: 数据库会话

    Returns:
        User: 当前用户对象

    Raises:
        HTTPException: Token无效或用户不存在
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # 验证Token
    payload = verify_token(token, token_type="access")
    if payload is None:
        raise credentials_exception

    user_id: int = int(payload.get("sub"))
    if user_id is None:
        raise credentials_exception

    # 获取用户
    user = AuthService.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用"
        )

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前活跃用户

    Args:
        current_user: 当前用户

    Returns:
        User: 当前活跃用户对象

    Raises:
        HTTPException: 用户不活跃
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户不活跃"
        )
    return current_user


async def get_current_superuser(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    获取当前超级用户

    Args:
        current_user: 当前用户

    Returns:
        User: 当前超级用户对象

    Raises:
        HTTPException: 用户不是超级用户
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user
