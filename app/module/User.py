from _ast import List

from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.Database import Base


class User(Base):
    __tablename__="ms_user"

    id:Mapped[int]=mapped_column(primary_key=True,comment="用户ID")
    username:Mapped[str]=mapped_column(String(50),unique=True,index=True,nullable=False,comment="用户名")
    email:Mapped[str]=mapped_column(String(100),unique=True,index=True,nullable=False,comment="邮箱")
    hashed_password:Mapped[str]=mapped_column(String(255),nullable=False,comment="hash 密码")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False,comment="是否在线")

    # 关系
    posts:Mapped["Post"]=relationship("Post",back_populates="author",cascade="all,delete-orphan")
    comments:Mapped[List["Comment"]]=relationship("Comment",back_populates="author",cascade="all,delete-orphan")












