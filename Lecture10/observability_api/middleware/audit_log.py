"""
middleware/audit_log.py
-----------------------
Audit Log — ghi lại các hành động nhạy cảm (write operations).

Trong production, audit log thường được ghi vào:
  - Một file riêng (audit.log) hoặc database.
  - Hệ thống SIEM (Security Information and Event Management).

Ở đây ta dùng Python logger riêng ghi vào file audit.log để minh họa.
"""

import logging
from pythonjsonlogger import jsonlogger
from flask import Flask, request, g


def _build_audit_logger() -> logging.Logger:
    audit_logger = logging.getLogger("audit")
    audit_logger.setLevel(logging.INFO)

    if audit_logger.handlers:
        return audit_logger

    handler = logging.FileHandler("audit.log", encoding="utf-8")
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        rename_fields={"asctime": "timestamp", "levelname": "level"},
    )
    handler.setFormatter(formatter)
    audit_logger.addHandler(handler)
    return audit_logger


_audit_logger = _build_audit_logger()

# Các method HTTP được coi là hành động ghi (write operations)
_WRITE_METHODS = {"POST", "PUT", "PATCH", "DELETE"}


def register_audit_log(app: Flask) -> None:
    """
    Đăng ký after_request hook để ghi audit log cho mọi write request.
    Hook này chạy SAU request_logger nên request_id đã có trong g.
    """

    @app.after_request
    def audit_write_operations(response):
        if request.method in _WRITE_METHODS:
            _audit_logger.info(
                "WRITE_OPERATION",
                extra={
                    "request_id": getattr(g, "request_id", "-"),
                    "method": request.method,
                    "path": request.path,
                    "status_code": response.status_code,
                    "remote_addr": request.remote_addr,
                    # Không log body thật (có thể chứa PII / credentials)
                    "content_length": request.content_length,
                },
            )
        return response
