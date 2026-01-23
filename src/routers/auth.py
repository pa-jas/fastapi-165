"""Authentication router - HTTP Basic Auth"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from config.auth import verify_credentials

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


class UserInfo(BaseModel):
    """User info response model"""
    username: str


@router.get("/me", response_model=UserInfo)
async def read_users_me(current_user: dict = Depends(verify_credentials)):
    """
    Get current user information
    Requires username and password via HTTP Basic Authentication
    """
    return {"username": current_user["username"]}
