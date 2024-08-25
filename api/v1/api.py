from fastapi import APIRouter, Depends, HTTPException
from .endpoints import campaigns, users
from config import settings
from models.user import User
from models.campaign import Campaign
import json
from mongoengine import connect, disconnect

api_router = APIRouter()
api_router.include_router(campaigns.router, prefix="/campaigns", tags=["campaigns"])
api_router.include_router(users.router, prefix="/users", tags=["users"])

@api_router.post("/reset-project", tags=["admin"])
async def reset_project():
    try:
        # Disconnect from the current database
        disconnect()
        # Reconnect to drop the database
        connect(db=settings.DATABASE_NAME, host=settings.MONGODB_URI)
        from mongoengine.connection import get_db
        db = get_db()
        db.client.drop_database(settings.DATABASE_NAME)
        # Reconnect to the fresh database
        connect(db=settings.DATABASE_NAME, host=settings.MONGODB_URI)
        return {
            "message": "Project reset successfully",
            "database_name": settings.DATABASE_NAME,
            "status": "Database dropped and reconnected"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reset project: {str(e)}")

@api_router.post("/initialize-db", tags=["admin"])
async def initialize_db():
    try:
        with open(settings.SAMPLE_DATA_FILE, 'r') as file:
            data = json.load(file)
        
        for user_data in data['users']:
            user = User(
                email=user_data['email'],
                full_name=user_data['full_name'],
                is_active=user_data['is_active']
            )
            user.set_password(user_data['password'])
            user.save()
        
        for campaign_data in data['campaigns']:
            campaign = Campaign(**campaign_data)
            campaign.save()
        
        return {"message": "Database initialized with sample data"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize database: {str(e)}")

# Add more routers for other endpoints
