"""
认证服务
"""
from typing import Optional
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token
)
from app.schemas.user import UserCreate, UserUpdate


class AuthService:
    """认证服务类"""

    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """
        根据用户名获取用户

        Args:
            db: 数据库会话
            username: 用户名

        Returns:
            Optional[User]: 用户对象，不存在则返回None
        """
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        根据邮箱获取用户

        Args:
            db: 数据库会话
            email: 邮箱

        Returns:
            Optional[User]: 用户对象，不存在则返回None
        """
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        根据ID获取用户

        Args:
            db: 数据库会话
            user_id: 用户ID

        Returns:
            Optional[User]: 用户对象，不存在则返回None
        """
        return db.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        """
        创建新用户

        Args:
            db: 数据库会话
            user_in: 用户创建数据

        Returns:
            User: 创建的用户对象

        Raises:
            ValueError: 如果用户名或邮箱已存在
        """
        # 检查用户名是否已存在
        if AuthService.get_user_by_username(db, user_in.username):
            raise ValueError("用户名已存在")

        # 检查邮箱是否已存在
        if AuthService.get_user_by_email(db, user_in.email):
            raise ValueError("邮箱已存在")

        # 创建用户
        db_user = User(
            username=user_in.username,
            email=user_in.email,
            password_hash=get_password_hash(user_in.password)
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate_user(
        db: Session,
        username: Optional[str] = None,
        email: Optional[str] = None,
        password: str = ""
    ) -> Optional[User]:
        """
        验证用户凭据

        Args:
            db: 数据库会话
            username: 用户名（可选）
            email: 邮箱（可选）
            password: 密码

        Returns:
            Optional[User]: 验证成功返回用户对象，失败返回None
        """
        # 优先使用用户名查找，其次使用邮箱
        user = None
        if username:
            user = AuthService.get_user_by_username(db, username)
        elif email:
            user = AuthService.get_user_by_email(db, email)

        if not user:
            return None

        # 验证密码
        if not verify_password(password, user.password_hash):
            return None

        return user

    @staticmethod
    def create_user_tokens(user: User) -> dict:
        """
        为用户创建访问令牌和刷新令牌

        Args:
            user: 用户对象

        Returns:
            dict: 包含 access_token 和 refresh_token 的字典
        """
        token_data = {"sub": str(user.id)}
        return {
            "access_token": create_access_token(token_data),
            "refresh_token": create_refresh_token(token_data),
            "token_type": "bearer"
        }

    @staticmethod
    def update_user(db: Session, user: User, user_in: UserUpdate) -> User:
        """
        更新用户信息

        Args:
            db: 数据库会话
            user: 用户对象
            user_in: 更新数据

        Returns:
            User: 更新后的用户对象
        """
        # 更新邮箱
        if user_in.email is not None:
            # 检查邮箱是否已被其他用户使用
            existing_user = AuthService.get_user_by_email(db, user_in.email)
            if existing_user and existing_user.id != user.id:
                raise ValueError("邮箱已被使用")
            user.email = user_in.email

        # 更新密码
        if user_in.password is not None:
            user.password_hash = get_password_hash(user_in.password)

        db.commit()
        db.refresh(user)
        return user
