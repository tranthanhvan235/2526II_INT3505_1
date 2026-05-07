from marshmallow import Schema, fields, validate

# --- Request schemas ---

class CreatePaymentRequestV1(Schema):
    amount      = fields.Int(
                    required=True,
                    validate=validate.Range(min=1)
                  )
    currency    = fields.Str(
                    required=True,
                    validate=validate.OneOf(['VND', 'USD', 'EUR'])
                  )
    card_number = fields.Str(required=True)                                 
    customer_id = fields.Str(required=True)


# --- Response schemas ---

class PaymentResponseV1(Schema):
    payment_id = fields.Str(dump_default='pay_abc123')
    status     = fields.Str()   
    amount     = fields.Int()
    currency   = fields.Str()