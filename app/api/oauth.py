"""
OAuth routes for dashboard login.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/login")
async def login():
    return {"message": "OAuth login to be implemented"}
