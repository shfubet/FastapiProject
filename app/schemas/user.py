from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    """用户基础 schema"""
    email: EmailStr
    name: str


class UserCreate(UserBase):
    """创建用户请求"""
    pass


class UserUpdate(BaseModel):
    """更新用户请求"""
    email: Optional[EmailStr] = None
    name: Optional[str] = None


class UserDetail(UserBase):
    """用户详情响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class UserList(BaseModel):
    """用户列表项"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    created_at: datetime


class UserListResponse(BaseModel):
    """用户列表分页响应"""
    items: List[UserList]
    total: int
    page: int
    page_size: int
