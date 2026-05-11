"""
metrics.py
----------
Khai báo các Prometheus metrics dùng chung trong toàn bộ app.

Metrics được export tại endpoint GET /metrics (xem app.py).

Loại metric sử dụng:
  - Counter   : đếm số lần xảy ra sự kiện (request, error)
  - Histogram : đo phân phối giá trị liên tục (latency, payload size)
  - Gauge     : giá trị tức thời có thể tăng/giảm (active connections)
"""

from prometheus_client import Counter, Histogram, Gauge

# ── Request counters ──────────────────────────────────────────────────────────
http_requests_total = Counter(
    name="http_requests_total",
    documentation="Tổng số HTTP request nhận được",
    labelnames=["method", "endpoint", "status_code"],
)

# ── Latency histogram ─────────────────────────────────────────────────────────
http_request_duration_seconds = Histogram(
    name="http_request_duration_seconds",
    documentation="Thời gian xử lý request (giây)",
    labelnames=["method", "endpoint"],
    # Buckets: 10ms → 10s
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# ── Error counter ─────────────────────────────────────────────────────────────
http_errors_total = Counter(
    name="http_errors_total",
    documentation="Số request trả về lỗi (status >= 400)",
    labelnames=["method", "endpoint", "status_code"],
)

# ── Rate-limit hit counter ────────────────────────────────────────────────────
rate_limit_hits_total = Counter(
    name="rate_limit_hits_total",
    documentation="Số lần request bị từ chối vì vượt rate limit",
    labelnames=["endpoint"],
)

# ── Active requests gauge ─────────────────────────────────────────────────────
active_requests = Gauge(
    name="active_requests",
    documentation="Số request đang được xử lý tại thời điểm hiện tại",
)
