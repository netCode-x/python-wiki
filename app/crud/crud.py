from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.module.comment import Comment
from app.module.post import Post
from app.module.user import User
from app.schemas.schemas import UserCreate, CommentCreate, PostCreate, PostUpdate
from app.utils.security import get_password_hash


# 根据用户ID 查询用户
async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().one_or_none()


# 根据用户名查找
async def get_user_by_username(db: AsyncSession, user_name: str):
    result = await db.execute(select(User).where(User.username == user_name))
    return result.scalars().one_or_none()

# 根据邮箱查找用户
async def get_user_by_email(db:AsyncSession, email: str):
    result =await  db.execute(select(User).where(User.email==email))
    return  result.scalars().one_or_none()

# 创建用户
async def create_user(db:AsyncSession,user:UserCreate):
    hashed =get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

# --- Post CRUD ---

async def get_posts(db:AsyncSession,skip:int=0,limit:int=100,published_only:bool =True):
    query = select(Post)
    if published_only:
        query= query.where(Post.is_published==True)
    query =query.offset(skip).limit(limit).order_by(Post.create_at.desc())
    result = await db.execute(query)


async def get_post(db: AsyncSession, post_id: int):
    result = await db.execute(select(Post).where(Post.id == post_id))
    return result.scalar_one_or_none()

async def create_post(db: AsyncSession, post: PostCreate, author_id: int):
    db_post = Post(**post.model_dump(), author_id=author_id)
    db.add(db_post)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def update_post(db: AsyncSession, post_id: int, post_update: PostUpdate):
    db_post = await get_post(db, post_id)
    if not db_post:
        return None
    update_data = post_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_post, key, value)
    await db.commit()
    await db.refresh(db_post)
    return db_post

async def delete_post(db: AsyncSession, post_id: int):
    db_post = await get_post(db, post_id)
    if db_post:
        await db.delete(db_post)
        await db.commit()
        return True
    return False

# --- Comment CRUD ---
async def get_comments_by_post(db: AsyncSession, post_id: int, skip: int = 0, limit: int = 100):
    result = await db.execute(
        select(Comment)
        .where(Comment.post_id == post_id)
        .offset(skip)
        .limit(limit)
        .order_by(Comment.created_at.desc())
    )
    return result.scalars().all()

async def create_comment(db: AsyncSession, comment: CommentCreate, author_id: int, post_id: int):
    db_comment = Comment(
        content=comment.content,
        author_id=author_id,
        post_id=post_id
    )
    db.add(db_comment)
    await db.commit()
    await db.refresh(db_comment)
    return db_comment

async def delete_comment(db: AsyncSession, comment_id: int):
    db_comment = await db.get(Comment, comment_id)
    if db_comment:
        await db.delete(db_comment)
        await db.commit()
        return True
    return False













