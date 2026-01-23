"""User management - In production, store users in database"""
from typing import Optional

# In-memory user store (replace with database in production)
# Format: username -> {"username": str, "password": str, "disabled": bool}
# NOTE: Using plain passwords for simplicity. In production, use password hashing!
USERS_DB = {
    "admin": {
        "username": "admin",
        "password": "admin123",  # Plain password - change this in production!
        "disabled": False,
    },
    "user": {
        "username": "user",
        "password": "user123",  # Plain password - change this in production!
        "disabled": False,
    }
}


def get_user(username: str) -> Optional[dict]:
    """Get user by username"""
    return USERS_DB.get(username)


def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Authenticate a user with username and password
    Returns user dict if valid, None otherwise
    """
    user = get_user(username)
    if not user:
        return None
    if user.get("disabled"):
        return None
    # Simple plain text password comparison
    if user.get("password") != password:
        return None
    return user
