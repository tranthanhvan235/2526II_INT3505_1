from flask import Blueprint, request, jsonify
from models import db, User, Order

crud_bp = Blueprint('crud', __name__)

# ==========================================
# Standard CRUD Methods for Users (Ch 7)
# ==========================================

@crud_bp.route('/users', methods=['POST'])
def create_user():
    """Create a new user (Standard Create Method)"""
    data = request.get_json()
    if not data or not 'username' in data or not 'email' in data:
        return jsonify({"error": "Missing username or email"}), 400
    
    if User.query.filter_by(username=data['username']).first() or User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User already exists"}), 409
        
    user = User(username=data['username'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify(user.to_dict()), 201

@crud_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retrieve a user (Standard Get Method)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200

@crud_bp.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    """Update a user (Standard Update Method)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    data = request.get_json()
    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
        
    db.session.commit()
    return jsonify(user.to_dict()), 200

@crud_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user (Standard Delete Method)"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
        
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200

# ==========================================
# Standard CRUD & Custom Methods for Orders (Ch 7-8)
# ==========================================

@crud_bp.route('/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    data = request.get_json()
    if not all(k in data for k in ("user_id", "product_name", "amount")):
        return jsonify({"error": "Missing required fields"}), 400
        
    order = Order(
        user_id=data['user_id'],
        product_name=data['product_name'],
        amount=data['amount']
    )
    db.session.add(order)
    db.session.commit()
    
    return jsonify(order.to_dict()), 201

@crud_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Retrieve an order"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order.to_dict()), 200

@crud_bp.route('/orders/<int:order_id>:cancel', methods=['POST'])
def cancel_order(order_id):
    """Cancel an order (Custom Method - Ch 8)"""
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Order not found"}), 404
        
    if order.status != 'PENDING':
        return jsonify({"error": f"Cannot cancel order in status: {order.status}"}), 400
        
    order.status = 'CANCELLED'
    db.session.commit()
    return jsonify(order.to_dict()), 200
