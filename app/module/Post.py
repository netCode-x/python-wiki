from sqlalchemy import String, Text, Boolean, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.Database import Base


class Post(Base):
    __tablename__= "ms_posts"

    id:Mapped[int]=mapped_column(primary_key=True,index=True,comment="postID")
    title:Mapped[str]=mapped_column(String(200),nullable=False,comment="文章")
    summary:Mapped[str]=mapped_column(String(500),comment="描述")
    content:Mapped[Text]=mapped_column(Text,nullable=False,comment="内容")
    is_published:Mapped[bool]=mapped_column(Boolean,default=True,comment="是否完成")
    author_id:Mapped[int]=mapped_column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False,comment="作者ID")

    # 关系绑定
    author:Mapped["User"]=relationship("User",back_populates="posts")
    comments:Mapped["Comment"]=relationship("Comment",back_populates="posts",cascade="all,delet-orphan")
















