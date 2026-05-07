from flask import jsonify, request
from marshmallow import Schema, fields, validate, ValidationError, validates
from datetime import datetime, timezone
import uuid
from . import v2

# ── Nested Schemas ────────────────────────────────────────
class AmountSchema(Schema):
    value    = fields.Decimal(required=True, as_string=True, validate=validate.Range(min=0))
    currency = fields.Str(required=True, validate=validate.OneOf(['VND', 'USD', 'EUR']))

class PaymentMethodSchema(Schema):
    type  = fields.Str(required=True, validate=validate.OneOf(['card', 'bank_transfer', 'wallet']))
    token = fields.Str(required=True)

class StatusSchema(Schema):
    code    = fields.Str()
    message = fields.Str()

class CreatePaymentV2(Schema):
    amount          = fields.Nested(AmountSchema, required=True)
    payment_method  = fields.Nested(PaymentMethodSchema, required=True)
    idempotency_key = fields.Str(required=True)
    metadata        = fields.Dict(keys=fields.Str(), load_default={})

    @validates('idempotency_key')
    def validate_idempotency_key(self, value, **kwargs):
        try:
            uuid.UUID(value)
        except ValueError:
            raise ValidationError('Must be a valid UUID v4')

req_schema = CreatePaymentV2()

# ── Routes ────────────────────────────────────────────────
@v2.route('/payments', methods=['POST'])
def create_payment():
    """
    [Chiến lược 1 — URL Path]
    POST /api/v2/payments
    Version xác định qua URL prefix /v2/
    """
    try:
        data = req_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify(err.messages), 400

    return jsonify({
        'strategy':        'URL Path versioning',
        'version':         'v2',
        'id':              'pay_' + uuid.uuid4().hex[:8],
        'status':          {'code': 'succeeded', 'message': 'Payment processed successfully'},
        'amount':          data['amount'],
        'idempotency_key': data['idempotency_key'],
        'created_at':      datetime.now(timezone.utc).isoformat(),
    }), 201


@v2.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    return jsonify({
        'strategy':   'URL Path versioning',
        'version':    'v2',
        'id':         payment_id,
        'status':     {'code': 'succeeded', 'message': 'Paid'},
        'amount':     {'value': '150000.00', 'currency': 'VND'},
        'created_at': datetime.now(timezone.utc).isoformat(),
    }), 200
