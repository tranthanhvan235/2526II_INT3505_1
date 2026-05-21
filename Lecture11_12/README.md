# Lecture 11 & 12: Advanced API Design Patterns

Dự án này triển khai các mẫu thiết kế API dựa trên cuốn sách của JJ Geewax (Chương 7–15). 
Ngôn ngữ/Framework: Python / Flask / SQLite.

## Các Mẫu Thiết Kế Được Triển Khai
1. **Standard Methods (CRUD)**: `GET, POST, PATCH, DELETE` cho resource `users` và `orders`.
2. **Custom Methods**: Endpoint `/api/orders/<id>:cancel` thực hiện logic nghiệp vụ mà không map trực tiếp 1-1 vào standard verbs.
3. **Query, Filtering, Pagination**: Danh sách `orders` có thể lọc theo `status`, `user_id` và hỗ trợ phân trang (limit/offset).
4. **HATEOAS**: Trong response của danh sách Orders trả về các link điều hướng (`self`, `next`, `prev`) và link thực thi action trên resource (`cancel`).
5. **Event-driven & Webhooks**: Endpoint nhận event từ Stripe (`payment_intent.succeeded`) và GitHub (`push`), kèm theo giả lập Notification System.

## Chạy Thử Ứng Dụng
```bash
# 1. Cài đặt dependencies
pip install -r requirements.txt

# 2. Khởi chạy Server
python app.py
# Server chạy ở http://localhost:5000
```

## Cấu Trúc Thư Mục
- `app.py`: Main entry point.
- `models.py`: Khai báo CSDL (User, Order) dùng SQLAlchemy.
- `api/crud.py`: Triển khai Standard CRUD + Custom Methods.
- `api/query.py`: Triển khai Filtering, Pagination, HATEOAS.
- `api/webhooks.py`: Triển khai Webhook receivers.
- `docs/API_Analysis.md`: Tài liệu so sánh REST/gRPC/GraphQL và phân tích API Stripe/GitHub.
