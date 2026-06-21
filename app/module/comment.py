from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base


class Comment(Base):
    __tablename__="ms_comments"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,index=True,comment="评论ID")
    content:Mapped[Text]=mapped_column(Text,nullable=False,comment="评论内容")
    author_id:Mapped[int]=mapped_column(Integer,ForeignKey("ms_user.id",ondelete="CASCADE"),nullable=False,comment="作者ID")
    post_id:Mapped[int]=mapped_column(Integer,ForeignKey("ms_posts.id",ondelete="CASCADE"),nullable=False,comment="postID")

     #  关系，告诉 SQLAlchemy 这两个关系是双向配对的。
     #  它让 ORM 知道当通过一端修改关系时，
     #  另一端的内存状态会自动同步，并且能帮助 SQLAlchemy 正确生成 JOIN 条件
    author:Mapped["User"]=relationship("User",back_populates="comments")
    post:Mapped["Post"]=relationship("Post",back_populates="comments")










