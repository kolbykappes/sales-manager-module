from fastapi import APIRouter
from .endpoints import campaigns, users

api_router = APIRouter()
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

# Add more routers for other endpoints
