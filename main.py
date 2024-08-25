from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect
from dotenv import load_dotenv
import os
from api.v1.api import api_router
from config import settings

load_dotenv()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# MongoDB connection
connect(host=settings.MONGODB_URI)

# Include API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
