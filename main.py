import logging
import os
from contextlib import asynccontextmanager
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.config.baseConfig import init_logging, settings
from app.config.redisConfig import get_redis
from app.db.database import Base, async_engine
from app.routes import users
from app.utils.logingMiddleware import RequestLogMiddleware

# 关闭 SQLAlchemy 详细日志
logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


# ---------- 生命周期管理 ----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logging.info("数据库表创建/检查完成")
        redis = await get_redis()
        await redis.ping()
        logging.info("Redis 连接成功")
    except Exception as e:
        logging.error(f"启动失败: {e}", exc_info=True)
        raise
    yield


# ---------- 创建应用 ----------
app = FastAPI(
    lifespan=lifespan,
    title="个人技术博客 API",
    version="1.0.0"
)

# CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 请求日志中间件（添加在路由之前，记录所有请求）
#app.add_middleware(RequestLogMiddleware)

# 注册路由
app.include_router(users.router)


@app.get("/")
async def root():
    return {"message": "欢迎访问个人技术博客"}


# ---------- 启动入口 ----------
if __name__ == "__main__":
    init_logging()  # 确保日志格式已配置
    port = int(os.getenv("PORT", settings.PORT))
    uvicorn.run(
        "main:app",
        host="127.0.0.1",       # 明确 IPv4，避免 localhost 解析问题
        port=port,
        reload=False,           # 生产环境关闭，开发时可改为 True
        access_log=False,       # 关闭 Uvicorn 自带访问日志，避免重复
        log_level=None          # 重要：让 Uvicorn 使用 root logger 的配置
    )