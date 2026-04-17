#!/usr/bin/env python3

import connexion

from openapi_server import encoder
from openapi_server.database import init_db, close_db


def main():
    # Cố gắng khởi tạo MongoDB (không bắt buộc)
    print("Starting server...")
    init_db()
    
    app = connexion.App(__name__, specification_dir='./openapi/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('openapi.yaml',
                arguments={'title': 'Book Management API'},
                pythonic_params=True)

    try:
        print("Server running on http://localhost:8080")
        app.run(port=8080)
    finally:
        close_db()


if __name__ == '__main__':
    main()
