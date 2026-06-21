from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.config import authConfig
from app.crud import crud
from app.db.database import get_database
from app.module.comment import Comment
from app.schemas import schemas

router = APIRouter(prefix="/comments", tags=["comments"])

@router.get("/posts/{post_id}", response_model=List[schemas.CommentResponse])
def list_comments(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_database)
):
    # 先检查文章是否存在
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comments = crud.get_comments_by_post(db, post_id, skip, limit)
    return comments

@router.post("/posts/{post_id}", response_model=schemas.CommentResponse, status_code=201)
def create_comment(
    post_id: int,
    comment: schemas.CommentCreate,
    db: Session = Depends(get_database()),
    current_user: schemas.UserResponse = Depends(authConfig.get_current_user)
):
    # 检查文章是否存在
    post = crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.create_comment(db, comment, current_user.id, post_id)

@router.delete("/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_database()),
    current_user: schemas.UserResponse = Depends(authConfig.get_current_user)
):
    # 只能删除自己的评论（或管理员，此处简化）
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if comment.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud.delete_comment(db, comment_id)
    return None









