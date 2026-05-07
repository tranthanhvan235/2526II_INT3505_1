from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
import uuid
from datetime import datetime, timezone

header_bp = Blueprint('header', __name__, url_prefix='/api/header')

# ── Helper ────────────────────────────────────────────────
def get_version():
    """Đọc version từ header X-API-Version (mặc định là 1)"""
    return request.headers.get('X-API-Version', '1').strip()

# ── Routes ────────────────────────────────────────────────
@header_bp.route('/payments', methods=['POST'])
def create_payment():
    """
    [Chiến lược 2 — Header versioning]
    POST /api/header/payments
    Header: X-API-Version: 1   →  logic v1
    Header: X-API-Version: 2   →  logic v2

    Ưu điểm: URL sạch, không đổi khi nâng version
    Nhược điểm: Khó test bằng browser, ít trực quan hơn
    """
    version = get_version()
    data    = request.get_json() or {}

    if version == '1':
        # Validate minimal v1
        if not data.get('amount') or not data.get('currency'):
            return jsonify({'error': 'amount and currency are required'}), 400

        return jsonify({
            'strategy':   'Header versioning  (X-API-Version: 1)',
            'version':    'v1',
            'payment_id': 'pay_header_v1_001',
            'status':     'success',
            'amount':     data['amount'],
            'currency':   data['currency'],
        }), 200

    elif version == '2':
        # Validate v2
        missing = [f for f in ['amount', 'payment_method', 'idempotency_key'] if f not in data]
        if missing:
            return jsonify({'error': f'Missing fields: {missing}'}), 400

        return jsonify({
            'strategy':        'Header versioning  (X-API-Version: 2)',
            'version':         'v2',
            'id':              'pay_' + uuid.uuid4().hex[:8],
            'status':          {'code': 'succeeded', 'message': 'Payment processed'},
            'amount':          data['amount'],
            'idempotency_key': data['idempotency_key'],
            'created_at':      datetime.now(timezone.utc).isoformat(),
        }), 201

    else:
        return jsonify({
            'error':             f'Unsupported API version: {version}',
            'supported_versions': ['1', '2'],
            'hint':              'Set header  X-API-Version: 1  or  X-API-Version: 2',
        }), 400


@header_bp.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    version = get_version()

    if version == '1':
        return jsonify({
            'strategy':   'Header versioning  (X-API-Version: 1)',
            'payment_id': payment_id,
            'status':     'success',
            'amount':     150000,
        }), 200
    else:
        return jsonify({
            'strategy':   'Header versioning  (X-API-Version: 2)',
            'id':         payment_id,
            'status':     {'code': 'succeeded', 'message': 'Paid'},
            'amount':     {'value': '150000.00', 'currency': 'VND'},
            'created_at': datetime.now(timezone.utc).isoformat(),
        }), 200
