from flask import Blueprint, request, jsonify, url_prefix
from models import db, Order

query_bp = Blueprint('query', __name__)

# ==========================================
# List, Filtering, Pagination & HATEOAS (Ch 9, 11)
# ==========================================

@query_bp.route('/orders', methods=['GET'])
def list_orders():
    """List orders with filtering and pagination"""
    # Filtering parameters
    status_filter = request.args.get('status')
    user_id_filter = request.args.get('user_id')
    
    # Pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Base query
    query = Order.query
    
    # Apply filters
    if status_filter:
        query = query.filter(Order.status == status_filter)
    if user_id_filter:
        query = query.filter(Order.user_id == user_id_filter)
        
    # Execute paginated query
    paginated_orders = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Format results
    items = []
    for order in paginated_orders.items:
        order_dict = order.to_dict()
        # Add HATEOAS links to individual resource
        order_dict["_links"] = {
            "self": f"/api/orders/{order.id}",
            "cancel": f"/api/orders/{order.id}:cancel" if order.status == 'PENDING' else None
        }
        items.append(order_dict)
        
    # Construct HATEOAS links for collection
    def build_url(p):
        from flask import url_for
        args = request.args.copy()
        args['page'] = p
        # url_for takes endpoint name, which is blueprint_name.function_name
        return url_for('query.list_orders', **args, _external=False)
        
    collection_links = {
        "self": build_url(page),
        "next": build_url(page + 1) if paginated_orders.has_next else None,
        "prev": build_url(page - 1) if paginated_orders.has_prev else None,
    }
    
    response = {
        "items": items,
        "metadata": {
            "total_items": paginated_orders.total,
            "total_pages": paginated_orders.pages,
            "current_page": page,
            "per_page": per_page
        },
        "_links": collection_links
    }
    
    return jsonify(response), 200
