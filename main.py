import logging
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.config.redisConfig import get_redis
from app.db.database import Base, async_engine
from app.routes import users

app = FastAPI(title="个人技术博客  API", version="1.0.0")


# CORS 配置（允许前端调用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 注册路由
app.include_router(users.router)


@app.on_event("startup")
async def startup():
    # 连接数据库创建数据库表（如果不存在）
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Database tables create/checked")
    # 2. 连接 Redis
    try:
        redis = await get_redis()
        await redis.ping()
        logging.info("Redis connected successfully")
    except Exception as e:
        logging.error(f"Redis connection failed: {e}")


@app.get("/")
async  def root():
    return {"message":"欢迎访问个人技术博客"}











