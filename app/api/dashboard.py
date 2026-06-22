"""
Dashboard API endpoints for frontend.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/repos")
async def get_repos():
    return {"repos": []}
