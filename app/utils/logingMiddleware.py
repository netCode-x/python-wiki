import logging
import time

from urllib.request import Request

from starlette.middleware.base import BaseHTTPMiddleware


# ---------- 自定义请求日志中间件（记录详细信息） ----------
class RequestLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        forwarded = request.headers.get("X-Forwarded-For")
        client_ip = forwarded.split(",")[0].strip() if forwarded else request.client.host
        response = await call_next(request)
        process_time = time.time() - start_time
        logging.info(
            f'{client_ip} - "{request.method} {request.url.path}" {response.status_code}'
            f'耗时: {process_time:.3f}s '
        )
        return response







