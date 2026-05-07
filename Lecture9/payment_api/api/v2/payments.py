from flask import request, jsonify, abort
from datetime import datetime, timezone
import uuid
from . import v2

@v2.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()

    idempotency_key = data.get('idempotency_key')
    if not idempotency_key:
        abort(400, description='idempotency_key is required')

    amount_obj = data.get('amount', {})
    value    = amount_obj.get('value')   
    currency = amount_obj.get('currency') 

    pm = data.get('payment_method', {})
    token = pm.get('token')

    now = datetime.now(timezone.utc).isoformat()

    return jsonify({
        'id':     'pay_' + uuid.uuid4().hex[:8],
        'status': {
            'code':    'succeeded',
            'message': 'Payment processed successfully',
        },
        'amount': {
            'value':    value,
            'currency': currency,
        },
        'idempotency_key': idempotency_key,
        'created_at':      now,
    }), 201


@v2.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    now = datetime.now(timezone.utc).isoformat()
    return jsonify({
        'id':        payment_id,
        'status':    {'code': 'succeeded', 'message': 'Paid'},
        'amount':    {'value': '150000.00', 'currency': 'VND'},
        'created_at': now,
    }), 200