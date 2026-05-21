# Phân tích API Design Patterns & So sánh Công nghệ

## 1. Khi nào dùng REST, gRPC, GraphQL?

### REST (Representational State Transfer)
- **Đặc điểm:** Dựa trên tài nguyên (resource-oriented), sử dụng HTTP verbs (GET, POST, PUT, DELETE) chuẩn mực.
- **Khi nào sử dụng:**
  - Khi xây dựng public API cho nhiều bên thứ 3 tích hợp (developer-friendly).
  - Khi cần khả năng cache mạnh mẽ (thông qua HTTP GET).
  - Ứng dụng CRUD đơn giản hoặc các hệ thống tuân thủ nghiêm ngặt HATEOAS.

### gRPC (gRPC Remote Procedure Calls)
- **Đặc điểm:** Dựa trên action/hàm (RPC), payload nhị phân (Protobuf), sử dụng HTTP/2.
- **Khi nào sử dụng:**
  - Giao tiếp nội bộ giữa các microservices cần tốc độ cao, độ trễ cực thấp.
  - Các thiết bị IoT có băng thông mạng giới hạn.
  - Không phù hợp lắm cho Public API trực tiếp lên trình duyệt (browser) vì cần proxy (gRPC-web).

### GraphQL
- **Đặc điểm:** Ngôn ngữ truy vấn linh hoạt, client quyết định chính xác data muốn lấy (tránh Over-fetching / Under-fetching).
- **Khi nào sử dụng:**
  - Frontend có UI phức tạp cần tổng hợp dữ liệu từ nhiều nguồn/bảng trong 1 request.
  - Khi API cần phục vụ nhiều loại client khác nhau (Mobile, Web, Desktop) với nhu cầu dữ liệu khác nhau.

---

## 2. Phân tích API của Stripe và GitHub (Tìm Patterns theo JJ Geewax)

### Stripe API (Fintech / Thanh toán)
- **Standard Methods (Chương 7):**
  - Stripe tuân thủ rất tốt các phương thức chuẩn (Create, Retrieve, Update, Delete, List).
  - Ví dụ: `POST /v1/customers` (Create), `GET /v1/customers/{id}` (Retrieve).
- **Custom Methods (Chương 8):**
  - Sử dụng các hành động cụ thể không map 1-1 với CRUD. Ví dụ: `POST /v1/payment_intents/{id}/cancel` (tương tự như `orders/:cancel` trong project này).
- **Pagination (Chương 11):**
  - Sử dụng **Cursor-based pagination** (thay vì offset/limit). API trả về `has_more: true/false` và dùng tham số `starting_after` hoặc `ending_before`.
- **Webhooks & Event-Driven (Chương 12-15):**
  - Event-driven mạnh mẽ. Mỗi khi một object thay đổi trạng thái (ví dụ: `payment_intent.succeeded`), Stripe bắn webhook payload sang server đăng ký. Payload chứa cả `type` và object `data` thay đổi.

### GitHub API (Developer Tools)
- **RESTful Resource & HATEOAS (Chương 7, 9):**
  - Resource rõ ràng (ví dụ: `GET /repos/{owner}/{repo}/issues`).
  - Hỗ trợ tốt HATEOAS thông qua HTTP `Link` header cho pagination (chứa rel="next", rel="last").
- **Filtering & Query (Chương 9):**
  - Cung cấp query mạnh mẽ qua endpoint `/search`. Ví dụ: `GET /search/repositories?q=language:python&sort=stars`.
- **Webhooks (Chương 12-15):**
  - Có cơ chế đăng ký Webhook theo repository hoặc organization. Sử dụng header đặc biệt `X-GitHub-Event` để chỉ định loại event (push, pull_request) và `X-Hub-Signature` để verify tính toàn vẹn của payload. 
- **GraphQL Adoption:**
  - GitHub cung cấp cả GraphQL API (v4) bên cạnh REST (v3) để giải quyết bài toán over-fetching khi truy xuất cây phụ thuộc phức tạp của Git.
