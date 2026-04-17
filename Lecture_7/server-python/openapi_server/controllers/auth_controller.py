import connexion
from typing import Dict
from typing import Tuple
from typing import Union
import jwt
from datetime import datetime, timedelta
from hashlib import sha256

from openapi_server.models.auth_response import AuthResponse  # noqa: E501
from openapi_server.models.error import Error  # noqa: E501
from openapi_server.models.login_request import LoginRequest  # noqa: E501
from openapi_server import util
from openapi_server.database import get_db, is_connected


def hash_password(password):
    """Hash password"""
    return sha256(password.encode()).hexdigest()


def login(body):  # noqa: E501
    """User Login

    Authenticate using email and password to receive a JWT Access Token. # noqa: E501

    :param login_request: 
    :type login_request: dict | bytes

    :rtype: Union[AuthResponse, Tuple[AuthResponse, int], Tuple[AuthResponse, int, Dict[str, str]]
    """
    login_request = body
    if connexion.request.is_json:
        login_request = LoginRequest.from_dict(connexion.request.get_json())  # noqa: E501
    
    # Kiểm tra kết nối MongoDB
    if not is_connected():
        return Error(code=503, message="Database service unavailable. Please start MongoDB."), 503
    
    # Lấy database
    db = get_db()
    if db is None:
        return Error(code=503, message="Database connection failed"), 503
    
    users_collection = db['users']
    
    # Tìm user trong MongoDB
    user = users_collection.find_one({'email': login_request.email})
    
    # Kiểm tra user và password
    if not user or user['password'] != hash_password(login_request.password):
        return Error(code=401, message="Invalid email or password"), 401
    
    # Tạo JWT token
    payload = {
        'user_id': str(user['_id']),
        'email': user['email'],
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, 'your-secret-key', algorithm='HS256')
    
    # Tạo response
    response = AuthResponse(
        access_token=token,
        token_type='Bearer',
        expires_in=86400
    )
    
    return response, 200
