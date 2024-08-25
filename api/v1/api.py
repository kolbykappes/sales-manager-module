from fastapi import APIRouter
from .endpoints import campaigns

api_router = APIRouter()
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])

# Add more routers for other endpoints
