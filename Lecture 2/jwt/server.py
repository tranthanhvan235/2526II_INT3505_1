import jwt
import datetime
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)
JWT_SECRET = "secret123"   
JWT_ALG = "HS256"         

USERS = {
    "admin": {"password": "admin", "role": "librarian"},
    "van": {"password": "van", "role": "user"}
}

def create_access_token(username, role):
    payload = {
        "sub": username,
        "role": role,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)  
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALG)

@app.post("/api/v1/auth/login")
def login():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "username and password are required"}), 400 

    user = USERS.get(username)
    if not user or user["password"] != password:
        return jsonify({"error": "Invalid username or password"}), 401 

    token = create_access_token(username, user["role"])
    
    return jsonify({
        "token": token, 
        "user": {"username": username, "role": user["role"]}
    }), 200 

def parse_bearer_token():
    auth = request.headers.get("Authorization")
    if not auth: return None
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1] 
    return None

def require_jwt(required_role=None):
    token = parse_bearer_token()
    if not token:
        return None, ("NOT_AUTHENTICATED", "Authorization Bearer token required", 401)
    
    try:
        claims = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALG])
        
        if required_role and claims.get("role") != required_role:
            return None, ("FORBIDDEN", "Insufficient permission", 403)
            
        return claims, None
    except jwt.ExpiredSignatureError:
        return None, ("TOKEN_EXPIRED", "Token expired", 401) 
    except jwt.InvalidTokenError:
        return None, ("INVALID_TOKEN", "Invalid token", 401)
    
@app.post("/api/v1/loans")
def create_loan():
    claims, error = require_jwt() 
    if error:
        return jsonify({"code": error[0], "message": error[1]}), error[2]

    user_id = claims["sub"]
    return jsonify({"message": f"User {user_id} borrowed book successfully"}), 201    

if __name__ == "__main__":
    app.run(debug=True, port=3005)