
import redis.asyncio as redis
from app.config.baseConfig import settings

_redis_client: redis.Redis | None = None

async def get_redis() -> redis.Redis:
    """获取 Redis 异步客户端（单例）"""
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}",
            username=settings.REDIS_USERNAME,
            password=settings.REDIS_PASSWORD,
            decode_responses=True,
            max_connections=10,           # 连接池大小，根据业务调整
            socket_timeout=5,             # 读/写超时（秒）
            socket_connect_timeout=5,     # 连接超时
            retry_on_timeout=True,        # 超时自动重试
            health_check_interval=30,     # 定期检查连接健康
        )
    return _redis_client

async def close_redis() -> None:
    """应用关闭时调用，释放连接池"""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None