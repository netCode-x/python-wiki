# 用于请求和响应的数据验证
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


# ------------ user schemas --------

class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    create_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True


class PostBase(BaseModel):
    title: str = Field(..., max_length=200)
    summary: Optional[str] = Field(None, max_length=500)
    content: str
    is_published: bool = True


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    summary: Optional[str] = Field(None, max_length=500)
    content: Optional[str]
    is_published: Optional[bool]


class PostResponse(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    author: Optional[UserResponse]  # 嵌套用户信息

    class Config:
        from_attributes = True


# --- Comment Schemas ---
class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    pass


class CommentResponse(CommentBase):
    id: int
    author_id: int
    post_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    author: Optional[UserResponse]

    class Config:
        from_attributes = True #它告诉 Pydantic：在验证数据时，允许从对象的属性（Attribute）中读取值，而不仅仅是从字典（Dict）中读取


# --- Token ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
