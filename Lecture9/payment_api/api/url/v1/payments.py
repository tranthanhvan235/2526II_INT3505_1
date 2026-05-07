from flask import jsonify, request
from marshmallow import Schema, fields, validate, ValidationError
from . import v1

# ── Schema ────────────────────────────────────────────────
class CreatePaymentV1(Schema):
    amount      = fields.Int(required=True, validate=validate.Range(min=1))
    currency    = fields.Str(required=True, validate=validate.OneOf(['VND', 'USD', 'EUR']))
    card_number = fields.Str(required=True)   # nhận card trực tiếp — legacy
    customer_id = fields.Str(load_default=None)

req_schema = CreatePaymentV1()

# ── Routes ────────────────────────────────────────────────
@v1.route('/payments', methods=['POST'])
def create_payment():
    """
    [Chiến lược 1 — URL Path]
    POST /api/v1/payments
    Version xác định qua URL prefix /v1/
    """
    try:
        data = req_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    return jsonify({
        'strategy':    'URL Path versioning',
        'version':     'v1',
        'payment_id':  'pay_legacy_001',
        'status':      'success',
        'amount':      data['amount'],
        'currency':    data['currency'],
        'note':        'Deprecated — migrate to /api/v2/payments',
    }), 200


@v1.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    return jsonify({
        'strategy':   'URL Path versioning',
        'version':    'v1',
        'payment_id': payment_id,
        'status':     'success',
        'amount':     150000,
    }), 200
