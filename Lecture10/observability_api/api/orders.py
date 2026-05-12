"""
api/orders.py
-------------
Blueprint "đơn hàng" — minh họa rate limit nghiêm ngặt hơn vì đây là
endpoint liên quan đến giao dịch tài chính (write-heavy, tốn tài nguyên).

Cũng minh họa pattern "circuit breaker" thủ công đơn giản bằng cách
theo dõi số lỗi liên tiếp và từ chối tạm thời khi vượt ngưỡng.
"""

import time
from flask import Blueprint, jsonify, request, g
from observability_api.logging_config import setup_logging

logger = setup_logging()

orders_bp = Blueprint("orders", __name__, url_prefix="/api/orders")

# Dữ liệu giả
_ORDERS: list[dict] = []
_ORDER_COUNTER = 0

# ── Circuit Breaker state (in-memory, minh họa) ──────────────────────────────
_CB_FAILURE_COUNT = 0          # số lỗi liên tiếp
_CB_LAST_FAILURE_TIME = 0.0    # timestamp lỗi cuối
_CB_OPEN_UNTIL = 0.0           # circuit mở đến lúc nào

CB_THRESHOLD = 3               # mở circuit sau 3 lỗi liên tiếp
CB_TIMEOUT = 30                # giây: thử lại sau 30 giây


def _is_circuit_open() -> bool:
    """Kiểm tra circuit breaker có đang mở (OPEN) không."""
    return time.time() < _CB_OPEN_UNTIL


def _record_failure():
    """Ghi nhận lỗi và mở circuit nếu vượt ngưỡng."""
    global _CB_FAILURE_COUNT, _CB_LAST_FAILURE_TIME, _CB_OPEN_UNTIL
    _CB_FAILURE_COUNT += 1
    _CB_LAST_FAILURE_TIME = time.time()
    if _CB_FAILURE_COUNT >= CB_THRESHOLD:
        _CB_OPEN_UNTIL = time.time() + CB_TIMEOUT
        logger.warning(
            "Circuit OPEN — downstream service unavailable",
            extra={"open_until": _CB_OPEN_UNTIL, "failure_count": _CB_FAILURE_COUNT},
        )


def _record_success():
    """Reset circuit breaker sau một lần thành công."""
    global _CB_FAILURE_COUNT, _CB_OPEN_UNTIL
    _CB_FAILURE_COUNT = 0
    _CB_OPEN_UNTIL = 0.0


# ── GET /api/orders ──────────────────────────────────────────────────────────
@orders_bp.route("", methods=["GET"])
def list_orders():
    """Lấy danh sách đơn hàng."""
    return jsonify({"orders": _ORDERS, "total": len(_ORDERS)}), 200


# ── POST /api/orders ─────────────────────────────────────────────────────────
@orders_bp.route("", methods=["POST"])
def create_order():
    """
    Tạo đơn hàng mới.

    Minh họa Circuit Breaker:
      - Nếu circuit OPEN → trả 503 Service Unavailable ngay.
      - Nếu circuit CLOSED → xử lý bình thường.
      - Nếu body có "force_error": true → giả lập lỗi downstream để test.
    """
    global _ORDER_COUNTER

    # --- Circuit Breaker check ---
    if _is_circuit_open():
        retry_after = int(_CB_OPEN_UNTIL - time.time()) + 1
        logger.error(
            "Circuit OPEN — request rejected",
            extra={"retry_after_seconds": retry_after},
        )
        return (
            jsonify({
                "error": "Service temporarily unavailable (circuit open)",
                "retry_after_seconds": retry_after,
            }),
            503,
        )

    data = request.get_json(silent=True) or {}

    # Giả lập lỗi downstream để test circuit breaker
    if data.get("force_error"):
        _record_failure()
        logger.error("Downstream payment service failed (simulated)")
        return jsonify({"error": "Payment service error (simulated)"}), 502

    # Xử lý bình thường
    if "product_id" not in data or "quantity" not in data:
        return jsonify({"error": "Fields 'product_id' and 'quantity' required"}), 422

    _ORDER_COUNTER += 1
    order = {
        "id": _ORDER_COUNTER,
        "product_id": data["product_id"],
        "quantity": data["quantity"],
        "request_id": getattr(g, "request_id", "-"),
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
    }
    _ORDERS.append(order)
    _record_success()

    logger.info("Order created", extra={"order_id": order["id"]})
    return jsonify(order), 201


# ── GET /api/orders/circuit-status ──────────────────────────────────────────
@orders_bp.route("/circuit-status", methods=["GET"])
def circuit_status():
    """Xem trạng thái circuit breaker (debug endpoint)."""
    status = "OPEN" if _is_circuit_open() else "CLOSED"
    return jsonify({
        "status": status,
        "failure_count": _CB_FAILURE_COUNT,
        "open_until": _CB_OPEN_UNTIL if _is_circuit_open() else None,
    }), 200
