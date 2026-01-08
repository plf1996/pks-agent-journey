"""
通用响应模式
"""
from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel, Field


T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """统一API响应格式"""

    code: int = Field(default=0, description="错误码，0表示成功")
    message: str = Field(default="success", description="响应消息")
    data: Optional[T] = Field(default=None, description="响应数据")

    class Config:
        """Pydantic配置"""
        json_schema_extra = {
            "example": {
                "code": 0,
                "message": "success",
                "data": {}
            }
        }


class PaginatedResponse(BaseModel, Generic[T]):
    """分页响应格式"""

    items: List[T] = Field(description="数据列表")
    total: int = Field(description="总记录数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页记录数")
    total_pages: int = Field(description="总页数")

    class Config:
        """Pydantic配置"""
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "total_pages": 5
            }
        }


class ErrorResponse(BaseModel):
    """错误响应格式"""

    code: int = Field(description="错误码")
    message: str = Field(description="错误信息")
    errors: Optional[dict] = Field(default=None, description="详细错误信息")

    class Config:
        """Pydantic配置"""
        json_schema_extra = {
            "example": {
                "code": 1001,
                "message": "参数错误",
                "errors": {
                    "field": ["错误详情"]
                }
            }
        }
