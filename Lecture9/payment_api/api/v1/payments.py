from flask import request, jsonify
from marshmallow import ValidationError
from . import v1
from .schemas import (
    CreatePaymentRequestV1,
    PaymentResponseV1,
)

req_schema = CreatePaymentRequestV1()
res_schema = PaymentResponseV1()

@v1.route('/payments', methods=['POST'])
def create_payment():
    try:
        # validate + deserialize input
        data = req_schema.load(
            request.get_json()
        )
    except ValidationError as err:
        return jsonify(err.messages), 400

    result = {
        'payment_id': 'pay_abc123',
        'status':     'success',
        'amount':     data['amount'],
        'currency':   data['currency'],
    }
    # serialize output
    return jsonify(
        res_schema.dump(result)
    ), 200