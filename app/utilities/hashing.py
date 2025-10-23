from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(password: str) -> str:
    """Convert a plain-text password into a hashed version for storage."""
    return generate_password_hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Check if a plain password matches the stored hash."""
    return check_password_hash(hashed, password)
