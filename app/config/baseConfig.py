import logging
import colorlog  # 需要先安装
import os
from pathlib import Path
from dotenv import load_dotenv, dotenv_values
from pydantic_settings import BaseSettings, SettingsConfigDict

# ---------- 日志和环境配置 ----------
_logging_initialized = False

def init_logging():
    global _logging_initialized
    if _logging_initialized:
        return

    # 1. 加载 .env 文件
    env_file = os.getenv("ENV_FILE", ".env.dev")
    load_dotenv(env_file)

    # 2. 获取日志级别
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, log_level, logging.INFO)

    # 3. 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # 清除已有的处理器（避免重复）
    if root_logger.handlers:
        root_logger.handlers.clear()

    # 4. 创建彩色格式器
    formatter = colorlog.ColoredFormatter(
        fmt='%(log_color)s%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(name)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # 5. 添加控制台处理器
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)

    # 6. 输出启动信息
    logging.info(f"加载环境配置: {env_file}")
    logging.info("配置加载完成")

    _logging_initialized = True

# ---------- 查找项目根目录 ----------
def find_project_root(start_path: Path) -> Path:
    for parent in [start_path] + list(start_path.parents):
        if (parent / ".env").exists():
            return parent
    raise FileNotFoundError("未找到 .env 文件，请确保项目根目录下存在 .env")


BASE_DIR = find_project_root(Path(__file__).resolve().parent)

# ---------- 合并环境配置（支持多环境） ----------
base_env = dotenv_values(BASE_DIR / ".env")
app_env = os.getenv("APP_ENV")
env_specific = {}
if app_env:
    env_file = BASE_DIR / f".env.{app_env}"
    if env_file.exists():
        env_specific = dotenv_values(env_file)
    else:
        logging.warning(f"环境文件 {env_file} 不存在，仅使用基础配置 .env")

merged_env = {**base_env, **env_specific}
for key, value in merged_env.items():
    if key not in os.environ:
        os.environ[key] = value


# ---------- Pydantic Settings ----------
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int

    PORT: int = 8000

    model_config = SettingsConfigDict(extra="ignore")


settings = Settings()
