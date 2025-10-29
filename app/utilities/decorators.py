from functools import wraps
from flask import request, jsonify
from app.utilities.jwt_helper import decode_token
from app.models.patient import Patient 

# TOKEN REQUIRED 
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"message": "Missing or invalid token"}), 401

        token = auth_header.split(" ")[1]
        payload = decode_token(token)

        if payload is None:
            return jsonify({"message": "Invalid token"}), 401

        if isinstance(payload, dict) and payload.get("error") == "expired":
            return jsonify({"message": "Token expired, please login again"}), 401

        # 🔍 Get patient from DB
        patient = Patient.query.get(payload.get("patient_id"))
        if not patient:
            return jsonify({"message": "User not found"}), 404

        # Pass patient object as current_user to the route
        return f(current_user=patient, *args, **kwargs)

    return decorated


def require_role(role):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")

            if not user:
                return jsonify({"message": "Authentication required"}), 401

            if getattr(user, "role", None) != role:
                return jsonify({"message": "Unauthorized role"}), 403

            return f(*args, **kwargs)
        return wrapper
    return decorator
