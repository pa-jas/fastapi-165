"""Authentication configuration - HTTP Basic Auth"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from config.users import authenticate_user

# HTTP Basic Auth scheme
security = HTTPBasic()


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)) -> dict:
    """
    Verify username and password using HTTP Basic Authentication
    Use this as a dependency to protect routes
    """
    user = authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return {"username": user["username"]}
