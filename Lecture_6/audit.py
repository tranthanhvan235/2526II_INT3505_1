import jwt
import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
SECRET_KEY = "SOA_SUPER_SECRET"

# In-memory database storing active Refresh Tokens
# Structure: { "username": "refresh_token_string" }
refresh_tokens_db = {}

def generate_access_token(username):
    payload = {
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=100) # Expires after 30s for easier testing
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def generate_refresh_token(username):
    payload = {
        'user': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7) # Expires after 7 days
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Assume user/password validation succeeds
    if username == 'admin' and password == '123':
        access_token = generate_access_token(username)
        refresh_token = generate_refresh_token(username)
        
        # Store Refresh Token in DB for management
        refresh_tokens_db[username] = refresh_token
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token
        })
    return jsonify({"msg": "Login failed"}), 401

@app.route('/refresh', methods=['POST'])
def refresh():
    data = request.json
    r_token = data.get('refresh_token')
    
    try:
        # 1. Decode refresh token
        decoded = jwt.decode(r_token, SECRET_KEY, algorithms=["HS256"])
        username = decoded['user']
        
        # 2. CHECK IN DB (Most important part of the Security Audit)
        if username not in refresh_tokens_db or refresh_tokens_db[username] != r_token:
            return jsonify({"msg": "Refresh Token is invalid or not exists!"}), 401
            
        # 3. Issue a new Access Token
        new_access_token = generate_access_token(username)
        return jsonify({'access_token': new_access_token})
        
    except:
        return jsonify({"msg": "Refresh Token is invalid or has expired"}), 401

@app.route('/logout', methods=['POST'])
def logout():
    username = request.json.get('username')
    # DELETE Refresh Token from DB -> This prevents Replay Attacks
    if username in refresh_tokens_db:
        del refresh_tokens_db[username]
    return jsonify({"msg": "Logout successful, old Refresh Token has been revoked!"})

@app.route('/protected', methods=['GET'])
def protected():
    auth_header = request.headers.get('Authorization')
    if not auth_header: return jsonify({"msg": "Missing token"}), 401
    
    token = auth_header.split(" ")[1]
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"msg": f"Hello {decoded['user']}, you have successfully used the Access Token!"})
    except jwt.ExpiredSignatureError:
        return jsonify({"msg": "Access Token has expired! Please use the Refresh Token."}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)