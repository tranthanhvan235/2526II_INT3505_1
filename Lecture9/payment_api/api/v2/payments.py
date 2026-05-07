from flask import request, jsonify
from marshmallow import ValidationError
from datetime import datetime, timezone
import uuid
from . import v2
from .schemas import (
    CreatePaymentRequestV2,
    PaymentResponseV2,
)

req_schema = CreatePaymentRequestV2()
res_schema = PaymentResponseV2()

@v2.route('/payments', methods=['POST'])
def create_payment():
    try:
        data = req_schema.load(
            request.get_json()
        )
    except ValidationError as err:
        return jsonify(err.messages), 400

    result = {
        'id': 'pay_' + uuid.uuid4().hex[:8],
        'status': {
            'code':    'succeeded',
            'message': 'Payment processed',
        },
        'amount':          data['amount'],
        'idempotency_key': data['idempotency_key'],
        'created_at':      datetime.now(timezone.utc),
    }
    return jsonify(
        res_schema.dump(result)
    ), 201