"""
logging_config.py
-----------------
Thiết lập Structured Logging (JSON format) cho Flask app.

Mục đích:
  - Mỗi log entry là một JSON object → dễ parse bởi Elasticsearch, Loki, v.v.
  - Ghi thêm metadata: timestamp, level, module, request_id.
"""

import logging
import sys
from pythonjsonlogger import jsonlogger


def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """
    Khởi tạo và trả về root logger với JSON formatter.

    Args:
        log_level: Mức log (DEBUG / INFO / WARNING / ERROR).

    Returns:
        Logger đã được cấu hình.
    """
    logger = logging.getLogger("observability_api")
    logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    # Tránh thêm handler trùng lặp khi reload
    if logger.handlers:
        return logger

    # --- Console handler (stdout) ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    # JSON formatter: liệt kê các field muốn có trong mỗi log line
    formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
        rename_fields={"asctime": "timestamp", "levelname": "level"},
    )
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- File handler (app.log) ---
    file_handler = logging.FileHandler("app.log", encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
