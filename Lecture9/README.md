# API Versioning Demo — Flask
## Cài đặt
```bash
pip install -r requirements.txt
python app.py
```

---

## Chiến lược 1: URL Path versioning
Version nằm trong URL — dễ nhìn, cache-friendly, phổ biến nhất.

### V1 (deprecated)
```bash
# POST — tạo payment
curl -i -X POST http://localhost:5000/api/v1/payments \
  -H "Content-Type: application/json" \
  -d '{"amount":150000,"currency":"VND","card_number":"4111111111111111","customer_id":"cus_123"}'

# GET — lấy payment
curl http://localhost:5000/api/v1/payments/pay_abc123
```

### V2 (current)
```bash
# POST — tạo payment
curl -X POST http://localhost:5000/api/v2/payments \
  -H "Content-Type: application/json" \
  -d '{
    "amount": {"value": "150000.00", "currency": "VND"},
    "payment_method": {"type": "card", "token": "tok_xyz"},
    "idempotency_key": "550e8400-e29b-41d4-a716-446655440000"
  }'

# GET — lấy payment
curl http://localhost:5000/api/v2/payments/pay_abc123
```

---

## Chiến lược 2: Header versioning
URL không đổi — version truyền qua header `X-API-Version`.

```bash
# V1 — truyền header X-API-Version: 1
curl -X POST http://localhost:5000/api/header/payments \
  -H "Content-Type: application/json" \
  -H "X-API-Version: 1" \
  -d '{"amount":150000,"currency":"VND"}'

# V2 — truyền header X-API-Version: 2
curl -X POST http://localhost:5000/api/header/payments \
  -H "Content-Type: application/json" \
  -H "X-API-Version: 2" \
  -d '{
    "amount": {"value": "150000.00", "currency": "VND"},
    "payment_method": {"type": "card", "token": "tok_xyz"},
    "idempotency_key": "550e8400-e29b-41d4-a716-446655440000"
  }'

# Không truyền header → mặc định V1
curl -X POST http://localhost:5000/api/header/payments \
  -H "Content-Type: application/json" \
  -d '{"amount":150000,"currency":"VND"}'

# Header không hợp lệ → trả lỗi
curl -X POST http://localhost:5000/api/header/payments \
  -H "Content-Type: application/json" \
  -H "X-API-Version: 99" \
  -d '{}'
```

---

## Chiến lược 3: Query Param versioning
Version truyền qua query string `?version=`.

```bash
# V1
curl -X POST "http://localhost:5000/api/query/payments?version=1" \
  -H "Content-Type: application/json" \
  -d '{"amount":150000,"currency":"VND"}'

# V2
curl -X POST "http://localhost:5000/api/query/payments?version=2" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": {"value": "150000.00", "currency": "VND"},
    "payment_method": {"type": "card", "token": "tok_xyz"},
    "idempotency_key": "550e8400-e29b-41d4-a716-446655440000"
  }'

# Không truyền param → mặc định V1
curl -X POST http://localhost:5000/api/query/payments \
  -H "Content-Type: application/json" \
  -d '{"amount":150000,"currency":"VND"}'
```

---

## So sánh nhanh 3 chiến lược

| Tiêu chí          | URL Path       | Header          | Query Param     |
|-------------------|---------------|-----------------|-----------------|
| Dễ nhìn           | ✅ Rất rõ      | ❌ Ẩn           | ✅ Thấy trên URL |
| Cache-friendly    | ✅             | ❌              | ⚠️ Tùy proxy    |
| RESTful           | ⚠️ Tranh cãi  | ✅ Đúng chuẩn   | ❌              |
| Dễ test browser   | ✅             | ❌ Cần tool     | ✅              |
| Dùng trong thực tế| Stripe, Twilio | GitHub          | Ít dùng         |
