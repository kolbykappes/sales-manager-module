import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect, DoesNotExist
from pymongo.errors import ConnectionFailure
from api.v1.api import api_router
from config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB connection
try:
    connect(db=settings.DATABASE_NAME, host=settings.MONGODB_URI)
    logger.info("Successfully connected to MongoDB")
except ConnectionFailure:
    logger.error("Failed to connect to MongoDB")
    raise

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# Add admin endpoints directly to the app
from api.v1.api import reset_project, initialize_db

app.post("/api/v1/reset-project", tags=["admin"])(reset_project)
app.post("/api/v1/initialize-db", tags=["admin"])(initialize_db)

@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}"}

@app.get("/health")
async def health_check():
    try:
        # Attempt to make a simple query to check the database connection
        from mongoengine.connection import get_db
        db = get_db()
        db.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Database is not available")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
