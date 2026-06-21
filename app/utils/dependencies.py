from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud import  crud


async def check_post_author(post_id: int, current_user_id: int, db: AsyncSession):
    post = await crud.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return post









