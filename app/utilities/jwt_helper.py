import jwt
import datetime
from flask import current_app

def create_token(data: dict, expires_in=3600):
    """Generate a JWT token for authentication."""
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token
import jwt
import datetime
from flask import current_app

def create_token(data: dict, expires_in=3600):
    """Generate a JWT token for authentication."""
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    payload["iat"] = datetime.datetime.utcnow()  # Issued at time

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    # Ensure token is string (PyJWT versions differ)
    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token


def decode_token(token: str):
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload

    except jwt.ExpiredSignatureError:
        # Token expired — return specific signal
        return {"error": "expired"}

    except jwt.InvalidTokenError:
        # Invalid token format/signature
        return None

def decode_token(token: str):
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
