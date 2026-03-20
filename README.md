# 2526II_INT3505_1

## 🚀 Deploy Vercel

Ứng dụng đã deploy trên Vercel:
- https://2526-ii-int-3505-1-three.vercel.app
- OpenAPI UI: https://2526-ii-int-3505-1-three.vercel.app/apidocs/

## 📦 Cấu trúc chính

- `Lecture_4/api/index.py`: Flask app chính, chứa CRUD route `/books`.
- `Lecture_4/vercel.json`: cấu hình Vercel Serverless Function.
- `Lecture_4/requirements.txt`: `flask`, `flasgger`.

## 🧪 Cách thử nghiệm API

1. GET tất cả sách:
   - `GET https://2526-ii-int-3505-1-three.vercel.app/books`
2. GET sách theo ID:
   - `GET https://2526-ii-int-3505-1-three.vercel.app/books/BK-2302`
3. Tạo sách mới:
   - `POST https://2526-ii-int-3505-1-three.vercel.app/books`
   - Body JSON:
     ```json
     {"title": "Tên sách", "author": "Tác giả", "publishedYear": 2026}
     ```
4. Cập nhật sách:
   - `PUT https://2526-ii-int-3505-1-three.vercel.app/books/BK-2302`
5. Xóa sách:
   - `DELETE https://2526-ii-int-3505-1-three.vercel.app/books/BK-2302`

## 🛠 Khắc phục lỗi thường gặp

- Lỗi 500: check logs Vercel, đảm bảo `requirements.txt` đúng và `vercel.json` có `builds` + `routes`.
- Lỗi 404 với `apidocs`: dùng URL `/apidocs/` trên Vercel và Python package `flasgger` đã cài.
