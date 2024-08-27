from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from mongoengine import connect, DoesNotExist, get_db
from pymongo.errors import ConnectionFailure
from loguru import logger
from api.v1.api import api_router
from config import settings
from log.extensions import configure_logger, loggable

configure_logger()

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# MongoDB connection and collection validation
@loggable(entry=True, exit=True, level="INFO")
def validate_collections():
    required_collections = ["users", "companies", "contacts", "campaigns", "emails"]
    missing_collections = []

    try:
        connect(db=settings.DATABASE_NAME, host=settings.MONGODB_URI)
        logger.info("Successfully connected to MongoDB")
        db = get_db()
        logger.info("get_db", database=db.name)
        existing_collections = db.list_collection_names()
        logger.info(f"Available collections: {existing_collections}")

        for collection in required_collections:
            if collection not in existing_collections:
                missing_collections.append(collection)
                logger.warning(
                    f"The '{collection}' collection does not exist in the database."
                )

        if missing_collections:
            logger.error(
                f"Missing collections: {', '.join(missing_collections)}. You need to initialize the database."
            )
        else:
            logger.info("All required collections are present in the database.")

    except ConnectionFailure as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to connect to MongoDB")
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to initialize database: {str(e)}"
        )

    return missing_collections


missing_collections = validate_collections()

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}"}


@app.get("/health")
async def health_check():
    try:
        # Attempt to make a simple query to check the database connection

        db = get_db()
        db.command("ping")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Database is not available")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
