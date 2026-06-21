from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

def find_env_file(start_path: Path) -> Path:
    # 从当前目录开始，向上逐级查找
    for parent in [start_path] + list(start_path.parents):
        env_path = parent / ".env"
        if env_path.exists():
            return env_path
    raise FileNotFoundError(".env not found")

# 使用示例
BASE_DIR = find_env_file(Path(__file__).resolve()).parent


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    # Redis 配置
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str

    # JWT 配置
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    # 在 Pydantic v2 / pydantic-settings 最新版中，官方推荐使用 model_config
    model_config = SettingsConfigDict(env_file=str(BASE_DIR / ".env"))

settings = Settings()