from functools import wraps
from flask import request, jsonify, g
from app.utilities.jwt_helper import decode_token

def require_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        # Check if Authorization header present & correctly formatted
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_token(token)

        # ✅ Distinguish invalid token vs expired token
        if payload is None:
            return jsonify({"message": "Invalid token"}), 401

        if isinstance(payload, dict) and payload.get("error") == "expired":
            return jsonify({"message": "Token expired, please login again"}), 401

        # ✅ Store user data globally for access in route functions
        g.user = payload
        return f(*args, **kwargs)
    return wrapper


def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = getattr(g, "user", None)

            # Ensure user is authenticated AND role is correct
            if not user:
                return jsonify({"message": "Authentication required"}), 401

            if user.get("role") != role:
                return jsonify({"message": "Unauthorized role"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
