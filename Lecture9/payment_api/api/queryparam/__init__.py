from flask import Blueprint, jsonify, request
import uuid
from datetime import datetime, timezone

query_bp = Blueprint('queryparam', __name__, url_prefix='/api/query')

# ── Helper ────────────────────────────────────────────────
def get_version():
    return request.args.get('version', '1').strip()

# ── Routes ────────────────────────────────────────────────
@query_bp.route('/payments', methods=['POST'])
def create_payment():
    version = get_version()
    data    = request.get_json() or {}

    if version == '1':
        if not data.get('amount') or not data.get('currency'):
            return jsonify({'error': 'amount and currency are required'}), 400

        return jsonify({
            'strategy':   'Query Param versioning  (?version=1)',
            'version':    'v1',
            'payment_id': 'pay_query_v1_001',
            'status':     'success',
            'amount':     data['amount'],
            'currency':   data['currency'],
        }), 200

    elif version == '2':
        missing = [f for f in ['amount', 'payment_method', 'idempotency_key'] if f not in data]
        if missing:
            return jsonify({'error': f'Missing fields: {missing}'}), 400

        return jsonify({
            'strategy':        'Query Param versioning  (?version=2)',
            'version':         'v2',
            'id':              'pay_' + uuid.uuid4().hex[:8],
            'status':          {'code': 'succeeded', 'message': 'Payment processed'},
            'amount':          data['amount'],
            'idempotency_key': data['idempotency_key'],
            'created_at':      datetime.now(timezone.utc).isoformat(),
        }), 201

    else:
        return jsonify({
            'error':             f'Unsupported version: {version}',
            'supported_versions': ['1', '2'],
            'hint':              'Use  ?version=1  or  ?version=2',
        }), 400


@query_bp.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    version = get_version()

    if version == '1':
        return jsonify({
            'strategy':   'Query Param versioning  (?version=1)',
            'payment_id': payment_id,
            'status':     'success',
            'amount':     150000,
        }), 200
    else:
        return jsonify({
            'strategy':   'Query Param versioning  (?version=2)',
            'id':         payment_id,
            'status':     {'code': 'succeeded', 'message': 'Paid'},
            'amount':     {'value': '150000.00', 'currency': 'VND'},
            'created_at': datetime.now(timezone.utc).isoformat(),
        }), 200
