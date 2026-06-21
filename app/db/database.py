from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from app.config.baseConfig import settings

# 数据库连接字符串 url
SQLALCHEMY_DATABASE_URL = (
    f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}"
    f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}?charset=utf8mb4"
)
# 创建异步数据库引擎（负责管理连接池和底层通信）
async_engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,                # 开启 SQL 日志输出（开发调试用，生产环境建议设为 False）
    pool_size=10,             # 连接池中保持的活跃连接数（常驻）
    max_overflow=20           # 当活跃连接用尽时，允许额外创建的连接数上限（超出后会阻塞等待）
)

# 创建异步会话工厂（用于生成 AsyncSession 实例）
# 每次调用 AsyncSessionLocal() 都会创建一个新的数据库会话
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,        # 绑定到上面创建的引擎
    class_=AsyncSession,      # 指定会话类（异步专用）
    expire_on_commit=False    # 提交后不使对象过期，避免下次访问时自动重新查询（性能优化）
)

# 定义模型基类（存放通用属性）
class Base(DeclarativeBase):
    create_at: Mapped[datetime]= mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="创建时间")
    update_at: Mapped[datetime]= mapped_column(DateTime,insert_default=func.now(),default=func.now,comment="更新时间")


# 定义异步依赖项函数（通常用于 FastAPI 等框架的依赖注入）
# 该函数会创建一个会话，并在请求处理完毕后自动提交、回滚或关闭
async def get_database():
    """
    异步数据库会话依赖项
    用法：在路由函数中用 Depends(get_database) 注入 AsyncSession
    """
    # 使用 async with 上下文管理器自动管理会话生命周期
    async with AsyncSessionLocal() as session:
        try:
            # 将会话对象交给调用方（如业务逻辑层）
            yield session
            # 如果业务逻辑执行成功，显式提交事务
            await session.commit()
        except Exception:
            # 如果发生异常，回滚事务，保证数据一致性
            await session.rollback()
            # 继续向上抛出异常，让上层处理
            raise
        finally:
            # 无论成功还是失败，最后都要关闭会话（释放连接回池）
            await session.close()