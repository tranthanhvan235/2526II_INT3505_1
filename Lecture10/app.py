"""
app.py
------
Flask application entry point — Buổi 10: Security & Monitoring.

Các tính năng được triển khai:
  ┌────────────────────────────────────────────────────────┐
  │  Observability                                         │
  │  ├─ Structured JSON Logging  (logging_config.py)      │
  │  ├─ Audit Log                (middleware/audit_log)   │
  │  ├─ Prometheus Metrics       (metrics.py)             │
  │  └─ Request tracing (X-Request-ID header)             │
  ├────────────────────────────────────────────────────────┤
  │  Security / Rate Limiting                             │
  │  ├─ Global limit:  200 req/ngày, 60 req/phút         │
  │  ├─ Endpoint /search: 10 req/phút                    │
  │  ├─ Endpoint POST /products: 5 req/phút              │
  │  └─ Endpoint POST /orders:  3 req/phút               │
  ├────────────────────────────────────────────────────────┤
  │  Reliability                                          │
  │  └─ Circuit Breaker (in-memory, xem api/orders.py)   │
  └────────────────────────────────────────────────────────┘

Endpoint metrics: GET /metrics  → Prometheus scrape target
"""

from flask import Flask, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from prometheus_client import make_wsgi_app, CONTENT_TYPE_LATEST, generate_latest
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from observability_api.logging_config import setup_logging
from observability_api.middleware.request_logger import register_request_logger
from observability_api.middleware.audit_log import register_audit_log
from observability_api.metrics import rate_limit_hits_total
from observability_api.api.products import products_bp
from observability_api.api.orders import orders_bp

# ── Logger ────────────────────────────────────────────────────────────────────
logger = setup_logging(log_level="DEBUG")

# ── Flask app ─────────────────────────────────────────────────────────────────
app = Flask(__name__)

# ── Rate Limiter (Flask-Limiter) ──────────────────────────────────────────────
# key_func: nhận diện client qua IP (có thể thay bằng API key / user_id)
# storage_uri: "memory://" = in-memory (dev). Dùng "redis://localhost:6379/0" cho production.
limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["200 per day", "60 per minute"],
    storage_uri="memory://",
)

# Áp dụng rate limit cụ thể cho từng route (override global limit)
# Products
limiter.limit("10 per minute")(products_bp.view_functions["products.search_products"])
limiter.limit("5 per minute")(products_bp.view_functions["products.create_product"])

# Orders
limiter.limit("3 per minute")(orders_bp.view_functions["orders.create_order"])


# ── Callback khi bị rate limited ─────────────────────────────────────────────
@app.errorhandler(429)
def ratelimit_handler(e):
    """Xử lý lỗi 429 Too Many Requests."""
    from flask import request as flask_request
    endpoint = flask_request.endpoint or flask_request.path
    rate_limit_hits_total.labels(endpoint=endpoint).inc()

    logger.warning(
        "Rate limit exceeded",
        extra={"endpoint": endpoint, "limit": str(e.description)},
    )
    return jsonify({
        "error": "Too Many Requests",
        "message": str(e.description),
        "retry_after": "Xem header Retry-After",
    }), 429


# ── Đăng ký middleware ────────────────────────────────────────────────────────
register_request_logger(app)   # Logging + Prometheus update
register_audit_log(app)        # Audit log cho write operations

# ── Đăng ký blueprints ────────────────────────────────────────────────────────
app.register_blueprint(products_bp)
app.register_blueprint(orders_bp)


# ── Health check ──────────────────────────────────────────────────────────────
@app.route("/health", methods=["GET"])
def health():
    """Liveness probe — load balancer / orchestrator gọi để kiểm tra app còn sống."""
    return jsonify({"status": "ok", "service": "observability-api"}), 200


# ── Prometheus metrics endpoint ───────────────────────────────────────────────
@app.route("/metrics", methods=["GET"])
def metrics():
    """
    Scrape endpoint cho Prometheus.
    Trả về text/plain theo định dạng Prometheus exposition format.
    """
    from flask import Response
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    logger.info("Starting Observability API", extra={"port": 5000})
    app.run(debug=True, port=5000)
