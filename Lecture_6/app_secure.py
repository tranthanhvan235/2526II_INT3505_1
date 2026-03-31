import jwt
import datetime
from flask import Flask, request, jsonify, make_response
from functools import wraps

app = Flask(__name__)
SECRET_KEY = "SOA_SECURE_KEY_2026"

# 1. Middleware to validate token from COOKIE and check scopes
def token_required(required_scope=None):
    def real_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # GET TOKEN FROM COOKIE (instead of Authorization header)
            token = request.cookies.get('access_token')

            if not token:
                return jsonify({'message': 'You are not logged in (missing cookie)!'}), 401
            
            try:
                data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
                # CHECK SCOPES (specific permissions)
                if required_scope and required_scope not in data.get('scopes', []):
                    return jsonify({'message': f'You do not have permission: {required_scope}'}), 403
                
                current_user = data['user']
            except:
                return jsonify({'message': 'Invalid or expired token!'}), 401
                
            return f(current_user, *args, **kwargs)
        return decorated
    return real_decorator

# 2. Login API - Set HttpOnly cookie
@app.route('/login', methods=['POST'])
def login():
    auth = request.json
    if auth['username'] == 'admin':
        # Grant admin permissions with multiple scopes
        scopes = ['profile:read', 'profile:edit', 'admin:full_access']
    else:
        # Regular users can only view
        scopes = ['profile:read']

    token = jwt.encode({
        'user': auth['username'],
        'scopes': scopes, # List of allowed actions
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, SECRET_KEY)

    # CREATE RESPONSE AND SET COOKIE
    resp = make_response(jsonify({'message': 'Login successful!'}))
    
    # httponly=True: JavaScript (XSS) cannot read this token
    # samesite='Lax'/'Strict': Protection against CSRF attacks
    resp.set_cookie('access_token', token, httponly=True, samesite='Lax')
    
    return resp

# 3. API that only requires profile view permission
@app.route('/view-profile', methods=['GET'])
@token_required(required_scope='profile:read')
def view(current_user):
    return jsonify({'data': f'This is the profile of {current_user}'})

# 4. API that requires edit permission (only admin has this scope)
@app.route('/edit-profile', methods=['POST'])
@token_required(required_scope='profile:edit')
def edit(current_user):
    return jsonify({'message': f'User {current_user} updated the profile successfully!'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)