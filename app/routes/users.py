import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import authConfig
from app.crud import crud
from app.db.database import get_database
from app.schemas import schemas
from app.utils.security import verify_password

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/register", response_model=schemas.UserResponse)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(get_database)):
    logging.info("收到的密码:", repr(user.password))
    logging.info("密码字节长度:", len(user.password.encode('utf-8')))
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)
async def login(user: schemas.UserLogin, db: AsyncSession = Depends(get_database)):
    db_user = await crud.get_user_by_username(db, username=user.username)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        logging.info(f"Incorrect username or password")
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = authConfig.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: schemas.UserResponse = Depends(authConfig.get_current_user)):
    return current_user









