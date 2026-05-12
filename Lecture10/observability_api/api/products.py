"""
api/products.py
---------------
Blueprint minh họa các endpoint "sản phẩm" với rate limiting khác nhau.

Rate limit được áp dụng theo 3 cấp độ:
  1. Global  : mọi endpoint đều bị giới hạn (cấu hình trong app.py)
  2. Per-Blueprint: tất cả route trong blueprint này
  3. Per-Route: giới hạn riêng cho route nhạy cảm (search, create)

Thư viện: Flask-Limiter (https://flask-limiter.readthedocs.io/)
"""

from flask import Blueprint, jsonify, request
from observability_api.logging_config import setup_logging

logger = setup_logging()

products_bp = Blueprint("products", __name__, url_prefix="/api/products")

# Dữ liệu giả — trong thực tế đây là DB query
_PRODUCTS = [
    {"id": 1, "name": "Laptop X1", "price": 25_000_000, "stock": 50},
    {"id": 2, "name": "Chuột không dây Z2", "price": 450_000, "stock": 200},
    {"id": 3, "name": "Bàn phím cơ K3", "price": 1_200_000, "stock": 80},
]


# ── GET /api/products ────────────────────────────────────────────────────────
# Rate limit: 60 request / phút (kế thừa global limit)
@products_bp.route("", methods=["GET"])
def list_products():
    """Lấy danh sách sản phẩm."""
    logger.info("Fetching product list", extra={"count": len(_PRODUCTS)})
    return jsonify({"products": _PRODUCTS, "total": len(_PRODUCTS)}), 200


# ── GET /api/products/search?q=<keyword> ────────────────────────────────────
# Rate limit riêng: 10 request / phút (endpoint tốn tài nguyên)
@products_bp.route("/search", methods=["GET"])
def search_products():
    """Tìm kiếm sản phẩm theo tên (rate-limited chặt hơn)."""
    keyword = request.args.get("q", "").strip().lower()

    if not keyword:
        return jsonify({"error": "Query param 'q' is required"}), 400

    results = [p for p in _PRODUCTS if keyword in p["name"].lower()]

    logger.info(
        "Product search",
        extra={"keyword": keyword, "result_count": len(results)},
    )
    return jsonify({"results": results, "keyword": keyword}), 200


# ── GET /api/products/<id> ───────────────────────────────────────────────────
@products_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id: int):
    """Lấy chi tiết một sản phẩm."""
    product = next((p for p in _PRODUCTS if p["id"] == product_id), None)

    if not product:
        logger.warning("Product not found", extra={"product_id": product_id})
        return jsonify({"error": f"Product {product_id} not found"}), 404

    return jsonify(product), 200


# ── POST /api/products ───────────────────────────────────────────────────────
# Rate limit riêng: 5 request / phút (write operation, tốn tài nguyên)
@products_bp.route("", methods=["POST"])
def create_product():
    """Tạo sản phẩm mới (write — sẽ được audit log ghi lại)."""
    data = request.get_json(silent=True)

    if not data or "name" not in data or "price" not in data:
        return jsonify({"error": "Fields 'name' and 'price' are required"}), 422

    new_product = {
        "id": max(p["id"] for p in _PRODUCTS) + 1,
        "name": data["name"],
        "price": data["price"],
        "stock": data.get("stock", 0),
    }
    _PRODUCTS.append(new_product)

    logger.info("Product created", extra={"product_id": new_product["id"]})
    return jsonify(new_product), 201
