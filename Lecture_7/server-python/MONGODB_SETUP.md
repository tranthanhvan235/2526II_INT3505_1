# Hướng dẫn kết nối PyMongo vào Server

## Cài đặt các gói cần thiết

```bash
# Cài đặt PyMongo, JWT và các thư viện cần thiết
cd /media/vanvan/D1/Study\ in\ UET/Nam-3/SOA/2526II_INT3505_1/Lecture_7/server-python
pip install -r requirements.txt
```

## Cấu hình MongoDB

### Option 1: Dùng MongoDB cục bộ
```bash
# Trên Linux
sudo systemctl start mongodb
# hoặc
mongod

# Chuẩn bị file .env
cp .env.example .env
# Hoặc tạo .env với nội dung:
# MONGO_URI=mongodb://localhost:27017
# DB_NAME=book_management
```

### Option 2: Dùng MongoDB Atlas (Cloud)
Thay đổi trong file `.env`:
```
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/book_management?retryWrites=true&w=majority
DB_NAME=book_management
```

## Seed dữ liệu mẫu

```bash
python seed_data.py
```

Kết quả:
```
✓ Users seeded
✓ Authors seeded
✓ Books seeded

All data seeded successfully!
```

## Chạy Server

```bash
# Từ thư mục server-python
python -m openapi_server

# Hoặc
python openapi_server/__main__.py
```

Server sẽ chạy ở: `http://localhost:8080`

## Test Login Endpoint

```bash
curl -X POST http://localhost:8080/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123"
  }'
```

## Cấu trúc Collections trong MongoDB

### users
```json
{
  "_id": ObjectId(...),
  "email": "user@example.com",
  "password": "sha256_hash",
  "name": "John Doe"
}
```

### authors
```json
{
  "_id": ObjectId(...),
  "name": "Author Name",
  "bio": "Author biography"
}
```

### books
```json
{
  "_id": ObjectId(...),
  "title": "Book Title",
  "description": "Book description",
  "author_id": "ObjectId_string",
  "isbn": "978-0-123456-78-9"
}
```

## Các file đã sửa đổi

1. **requirements.txt** - Thêm pymongo, PyJWT, python-dotenv
2. **openapi_server/database.py** - File mới để quản lý kết nối MongoDB
3. **openapi_server/__main__.py** - Thêm khởi tạo database
4. **openapi_server/controllers/auth_controller.py** - Sử dụng PyMongo cho authentication
5. **.env.example** - File cấu hình mẫu
6. **seed_data.py** - Script để seed dữ liệu mẫu

## Lưu ý quan trọng

- Thay đổi `JWT_SECRET` trong production
- Sử dụng password hashing tốt hơn (bcrypt) cho production
- Cấu hình CORS nếu frontend chạy trên domain khác
- Thêm validation cho input data
