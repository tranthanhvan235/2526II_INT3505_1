# Buổi 10 — Service Operation: Security & Monitoring

Thực hành Flask với:
- **Structured Logging** (JSON format, ghi ra console + file)
- **Audit Log** (ghi lại mọi write operation)
- **Prometheus Metrics** (Counter, Histogram, Gauge)
- **Rate Limiting** (global + per-route, dùng Flask-Limiter)
- **Circuit Breaker** (in-memory, minh họa trong Orders API)
- **Request Tracing** (X-Request-ID header)

---

## Cấu trúc thư mục

```
Lecture10/
├── app.py                          # Entry point, cấu hình rate limiter
├── requirements.txt
└── observability_api/
    ├── logging_config.py           # JSON logger (console + app.log)
    ├── metrics.py                  # Prometheus metrics definitions
    ├── middleware/
    │   ├── request_logger.py       # Log req/resp + cập nhật Prometheus
    │   └── audit_log.py           # Audit log → audit.log
    └── api/
        ├── products.py            # CRUD sản phẩm (rate limit khác nhau)
        └── orders.py              # Tạo đơn hàng + Circuit Breaker
```

---

## Cài đặt & chạy

```bash
cd Lecture10
pip install -r requirements.txt
python app.py
```

Server chạy tại `http://localhost:5000`

---

## Phần 1 — Structured Logging

Mỗi request sẽ in ra console theo dạng JSON:

```json
{"timestamp": "2026-05-13T16:00:00", "name": "observability_api", "level": "INFO",
 "message": "Incoming request", "method": "GET", "path": "/api/products",
 "request_id": "f47ac10b-...", "remote_addr": "127.0.0.1"}
```

Đồng thời ghi vào file `app.log` (level INFO trở lên).

### Test logging

```bash
# Gọi bất kỳ endpoint nào → quan sát console / app.log
curl http://localhost:5000/api/products

# Xem file log
cat app.log
```

---

## Phần 2 — Audit Log

Mọi request **POST / PUT / PATCH / DELETE** đều được ghi thêm vào `audit.log`.

```bash
# Tạo sản phẩm → ghi audit log
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Tai nghe Bluetooth B5", "price": 800000, "stock": 30}'

# Xem audit log
cat audit.log
```

Mỗi entry trong `audit.log`:

```json
{"timestamp": "2026-05-13T16:00:05", "name": "audit", "level": "INFO",
 "message": "WRITE_OPERATION", "method": "POST", "path": "/api/products",
 "status_code": 201, "remote_addr": "127.0.0.1", "content_length": 58}
```

---

## Phần 3 — Prometheus Metrics

### Scrape endpoint

```bash
curl http://localhost:5000/metrics
```

### Các metric được export

| Metric | Loại | Ý nghĩa |
|--------|------|---------|
| `http_requests_total` | Counter | Tổng request theo method/endpoint/status |
| `http_request_duration_seconds` | Histogram | Phân phối latency |
| `http_errors_total` | Counter | Tổng lỗi (status ≥ 400) |
| `rate_limit_hits_total` | Counter | Số lần bị rate limit |
| `active_requests` | Gauge | Request đang xử lý |

### Tạo traffic và xem metrics

```bash
# Tạo một vài request
curl http://localhost:5000/api/products
curl http://localhost:5000/api/products/1
curl http://localhost:5000/api/products/999  # → 404 (error)
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 2}'

# Xem metrics Prometheus
curl http://localhost:5000/metrics | grep http_
```

---

## Phần 4 — Rate Limiting

### Cấu hình rate limit

| Scope | Endpoint | Giới hạn |
|-------|----------|----------|
| Global | Tất cả | 200/ngày · 60/phút |
| Per-route | `GET /api/products/search` | **10/phút** |
| Per-route | `POST /api/products` | **5/phút** |
| Per-route | `POST /api/orders` | **3/phút** |

### Test rate limit — Search endpoint (10 req/phút)

Chạy vòng lặp 12 lần → lần thứ 11 sẽ bị 429:

```bash
# Windows PowerShell
for ($i=1; $i -le 12; $i++) {
  $r = Invoke-WebRequest -Uri "http://localhost:5000/api/products/search?q=laptop" -UseBasicParsing
  Write-Host "[$i] Status: $($r.StatusCode)"
}
```

```bash
# Linux / macOS / Git Bash
for i in $(seq 1 12); do
  code=$(curl -s -o /dev/null -w "%{http_code}" \
    "http://localhost:5000/api/products/search?q=laptop")
  echo "[$i] Status: $code"
done
```

Response khi bị rate limit:

```json
{
  "error": "Too Many Requests",
  "message": "10 per 1 minute",
  "retry_after": "Xem header Retry-After"
}
```

### Test rate limit — Tạo đơn hàng (3 req/phút)

```bash
# Gọi 4 lần liên tiếp → lần 4 bị 429
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 1}'
```

---

## Phần 5 — Circuit Breaker

Circuit Breaker trong `api/orders.py` hoạt động theo 3 trạng thái:

```
CLOSED (bình thường) → [≥3 lỗi liên tiếp] → OPEN (từ chối request)
      ↑                                              │
      └──────── [sau 30 giây, thử lại] ─────────────┘
                        HALF-OPEN
```

### Test Circuit Breaker

**Bước 1 — Xem trạng thái ban đầu (CLOSED)**

```bash
curl http://localhost:5000/api/orders/circuit-status
# {"status": "CLOSED", "failure_count": 0, "open_until": null}
```

**Bước 2 — Giả lập 3 lỗi liên tiếp để mở circuit**

```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"force_error": true}'

curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"force_error": true}'

curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"force_error": true}'
```

**Bước 3 — Xem circuit đã OPEN**

```bash
curl http://localhost:5000/api/orders/circuit-status
# {"status": "OPEN", "failure_count": 3, "open_until": 1747145430.5}
```

**Bước 4 — Thử tạo đơn hàng khi circuit OPEN → bị từ chối ngay (503)**

```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"product_id": 1, "quantity": 1}'
# {"error": "Service temporarily unavailable (circuit open)", "retry_after_seconds": 29}
```

**Bước 5 — Chờ 30 giây rồi thử lại → circuit tự CLOSE lại**

---

## Phần 6 — Request Tracing (X-Request-ID)

Mỗi request được gắn một ID duy nhất.  
Client có thể tự truyền ID vào để trace end-to-end:

```bash
curl -H "X-Request-ID: my-custom-trace-001" \
  http://localhost:5000/api/products

# Response sẽ có header: X-Request-ID: my-custom-trace-001
# Log sẽ ghi: "request_id": "my-custom-trace-001"
```

---

## Health Check

```bash
curl http://localhost:5000/health
# {"status": "ok", "service": "observability-api"}
```

---

## Tổng kết kiến thức

| Chủ đề | Tool / Pattern | File |
|--------|---------------|------|
| Structured Logging | `python-json-logger` | `logging_config.py` |
| Audit Log | Python `logging` + file handler | `middleware/audit_log.py` |
| Metrics | `prometheus-client` | `metrics.py` |
| Rate Limiting | `flask-limiter` | `app.py` |
| Circuit Breaker | In-memory state machine | `api/orders.py` |
| Request Tracing | `X-Request-ID` header | `middleware/request_logger.py` |
