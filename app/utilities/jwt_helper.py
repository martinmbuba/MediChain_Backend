import jwt
import datetime
from flask import current_app

def create_token(data: dict, expires_in=3600):
    """Generate a JWT token for authentication."""
    payload = data.copy()
    payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(seconds=expires_in)
    payload["iat"] = datetime.datetime.utcnow()  

    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    if isinstance(token, bytes):
        token = token.decode("utf-8")

    return token


def decode_token(token: str):
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload

    except jwt.ExpiredSignatureError:
        return {"error": "expired"}

    except jwt.InvalidTokenError:
        return None
