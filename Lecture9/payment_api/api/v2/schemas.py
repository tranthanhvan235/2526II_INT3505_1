from marshmallow import Schema, fields, validate, validates, ValidationError
import uuid

# --- Nested schemas ---

class AmountSchema(Schema):
    value    = fields.Decimal(
                 required=True, as_string=True,
                 validate=validate.Range(min=0)
               )                           
    currency = fields.Str(
                 required=True,
                 validate=validate.OneOf(['VND', 'USD', 'EUR'])
               )

class PaymentMethodSchema(Schema):
    type  = fields.Str(
              required=True,
              validate=validate.OneOf(['card', 'bank_transfer', 'wallet'])
            )
    token = fields.Str(required=True) 

class StatusSchema(Schema):
    code    = fields.Str()
    message = fields.Str()


# --- Request schemas ---

class CreatePaymentRequestV2(Schema):
    amount          = fields.Nested(AmountSchema, required=True)
    payment_method  = fields.Nested(PaymentMethodSchema, required=True)
    idempotency_key = fields.Str(required=True)
    metadata        = fields.Dict(keys=fields.Str(), load_default={})

    @validates('idempotency_key')
    def validate_idempotency_key(self, value):
        try:
            uuid.UUID(value)          
        except ValueError:
            raise ValidationError('Must be a valid UUID v4')


# --- Response schemas ---

class PaymentResponseV2(Schema):
    id              = fields.Str()
    status          = fields.Nested(StatusSchema)
    amount          = fields.Nested(AmountSchema)
    idempotency_key = fields.Str()
    created_at      = fields.DateTime()