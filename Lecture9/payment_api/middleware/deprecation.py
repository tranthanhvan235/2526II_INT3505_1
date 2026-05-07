from flask import request
from datetime import datetime

V1_DEPRECATED_DATE = "Sat, 01 May 2025 00:00:00 GMT"
V1_SUNSET_DATE     = "Fri, 28 Nov 2025 00:00:00 GMT"
V2_DOCS_URL        = "https://docs.paygate.vn/v2"

def add_deprecation_headers(response):
    """
    Tự động thêm Deprecation + Sunset header
    vào MỌI response của /api/v1/* 
    """
    if request.path.startswith('/api/v1/'):
        response.headers['Deprecation'] = V1_DEPRECATED_DATE
        response.headers['Sunset']      = V1_SUNSET_DATE
        response.headers['Link'] = (
            f'<{V2_DOCS_URL}>; rel="successor-version"'
        )
    return response