"""
middleware/request_logger.py
----------------------------
Flask middleware (before/after request hooks) để:
  1. Gắn request_id duy nhất vào mỗi request (dùng cho distributed tracing đơn giản).
  2. Log thông tin request đầu vào và response đầu ra theo dạng JSON.
  3. Cập nhật Prometheus metrics sau mỗi request.
"""

import time
import uuid
from flask import Flask, g, request, Response
from observability_api.logging_config import setup_logging
from observability_api.metrics import (
    http_requests_total,
    http_request_duration_seconds,
    http_errors_total,
    active_requests,
)

logger = setup_logging()


def register_request_logger(app: Flask) -> None:
    """Đăng ký before/after request hooks vào Flask app."""

    @app.before_request
    def before_request():
        # Tạo request_id để trace xuyên suốt một request
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        g.start_time = time.perf_counter()

        # Tăng gauge active requests
        active_requests.inc()

        logger.info(
            "Incoming request",
            extra={
                "request_id": g.request_id,
                "method": request.method,
                "path": request.path,
                "remote_addr": request.remote_addr,
                "user_agent": request.user_agent.string,
            },
        )

    @app.after_request
    def after_request(response: Response) -> Response:
        # Gắn request_id vào response header để client dễ trace
        response.headers["X-Request-ID"] = getattr(g, "request_id", "-")

        # Tính latency
        duration = time.perf_counter() - getattr(g, "start_time", time.perf_counter())
        endpoint = request.endpoint or request.path

        # Cập nhật Prometheus
        http_requests_total.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=str(response.status_code),
        ).inc()

        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(duration)

        if response.status_code >= 400:
            http_errors_total.labels(
                method=request.method,
                endpoint=endpoint,
                status_code=str(response.status_code),
            ).inc()

        # Giảm gauge active requests
        active_requests.dec()

        logger.info(
            "Request completed",
            extra={
                "request_id": getattr(g, "request_id", "-"),
                "method": request.method,
                "path": request.path,
                "status_code": response.status_code,
                "duration_ms": round(duration * 1000, 2),
            },
        )

        return response
