from flask import request, jsonify
from . import v1

@v1.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()

    amount   = data.get('amount')       
    currency = data.get('currency')     
    card_no  = data.get('card_number') 

    return jsonify({
        'payment_id': 'pay_abc123',
        'status':     'success',    
        'amount':     amount,        
        'currency':   currency,
    }), 200


@v1.route('/payments/<payment_id>', methods=['GET'])
def get_payment(payment_id):
    return jsonify({
        'payment_id': payment_id,
        'status':     'success',
        'amount':     150000,
    }), 200