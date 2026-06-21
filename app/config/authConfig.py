from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.baseConfig import settings
from app.crud import crud
from app.db.database import get_database
from app.schemas import schemas

#创建一个“密码加密与验证的总控台”。它负责统一管理“如何加密密码”和“如何验证密码”这两件事
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login") # 我们将定义此路由




def create_access_token(data:dict,expires_delta:Optional[timedelta] =None)-> str:
    to_encode=data.copy()
    # 计算过期时间
    if expires_delta:
        expire=datetime.now(timezone.utc) + expires_delta
    else:
        expire= datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    #加密编码生成 Token：
    encoded_jwt=jwt.encode(to_encode,settings.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_database)
) -> schemas.UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await crud.get_user_by_username(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user
















