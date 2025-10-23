from functools import wraps
from flask import request, jsonify
from app.utilities.jwt_helper import decode_token

def require_auth(f):
    """Decorator to ensure a request has a valid JWT token."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        if not payload:
            return jsonify({"message": "Invalid or expired token"}), 401

        request.user = payload
        return f(*args, **kwargs)
    return wrapper

def require_role(role):
    """Decorator to ensure the logged-in user has the correct role (e.g., 'doctor', 'patient')."""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = getattr(request, "user", None)
            if not user or user.get("role") != role:
                return jsonify({"message": "Unauthorized role"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
