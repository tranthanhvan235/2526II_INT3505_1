import jwt
import datetime
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)
SECRET_KEY = "SOA_KEY_2026"

def token_required(allowed_roles=None):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                # Bearer <token>
                token = request.headers['Authorization'].split(" ")[1]

            if not token:
                return jsonify({'message': 'Missing Token!'}), 401
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                # Role
                if allowed_roles and data['role'] not in allowed_roles:
                    return jsonify({'message': 'No access!'}), 403
                current_user = data['user']
            except jwt.ExpiredSignatureError:
                return jsonify({'message': 'Token expired!'}), 401
            except:
                return jsonify({'message': 'Token is invalid!'}), 401
            
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if auth['username'] == 'admin':
        role = 'admin'
    else:
        role = 'user'

    token = jwt.encode({
        'user': auth['username'],
        'role': role, 
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=1) 
    }, SECRET_KEY)
    
    return jsonify({'access_token': token})

@app.route('/admin-only', methods=['GET'])
@token_required(allowed_roles=['admin'])
def admin_data(current_user):
    return jsonify({'message': f'Hello Admin {current_user}, this is secret data!'})

if __name__ == '__main__':
    app.run(port=5000)