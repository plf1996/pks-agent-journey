"""
用户相关的Pydantic模式
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, validator, model_validator


class UserBase(BaseModel):
    """用户基础模式"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")


class UserCreate(UserBase):
    """用户创建模式"""

    password: str = Field(..., min_length=8, description="密码")

    @validator('username')
    def validate_username(cls, v):
        """验证用户名格式"""
        import re
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('用户名只能包含字母、数字和下划线')
        return v

    @validator('password')
    def validate_password(cls, v):
        """验证密码强度"""
        if not any(c.isalpha() for c in v):
            raise ValueError('密码必须包含字母')
        if not any(c.isdigit() for c in v):
            raise ValueError('密码必须包含数字')
        return v


class UserUpdate(BaseModel):
    """用户更新模式"""

    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)


class UserInDB(UserBase):
    """数据库中的用户模式"""

    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        """Pydantic配置"""
        from_attributes = True


class UserResponse(UserInDB):
    """用户响应模式"""

    pass


class Token(BaseModel):
    """Token响应模式"""

    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="bearer", description="令牌类型")


class TokenPayload(BaseModel):
    """Token负载模式"""

    sub: int = Field(..., description="用户ID")
    exp: int = Field(..., description="过期时间")
    type: str = Field(..., description="令牌类型")


class LoginRequest(BaseModel):
    """登录请求模式"""

    username: Optional[str] = Field(None, description="用户名")
    email: Optional[EmailStr] = Field(None, description="邮箱")
    password: str = Field(..., description="密码")

    @model_validator(mode='after')
    def validate_username_or_email(self):
        """验证至少提供用户名或邮箱之一"""
        if not self.username and not self.email:
            raise ValueError('必须提供用户名或邮箱')
        return self


class UserWithToken(UserResponse):
    """包含Token的用户响应模式"""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
