import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect, ConnectionError
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
except ConnectionError:
    logger.error("Failed to connect to MongoDB")
    raise

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
