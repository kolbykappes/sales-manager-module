# Backend Coding Guidelines

## FastAPI
- Organize endpoints into separate files under `api/v1/endpoints/`.
- Use Pydantic models for request/response schemas.
- Implement proper input validation using Pydantic models.
- Use async functions for database operations and external API calls.
- Implement proper error handling and use FastAPI's HTTPException for API errors.
- Use dependency injection for shared resources (e.g., database connections, settings).
- Utilize the `settings` object from `config.py` for accessing configuration values.

## Environment Variables
- Use the `python-dotenv` library to load environment variables from a .env file in development.
- In production, set environment variables according to the deployment platform's best practices.
- Never commit the .env file to version control; use .env.example as a template.

## Database (MongoDB with MongoEngine)
- Define document models in separate files under the `models/` directory.
- Use MongoEngine's Document class for defining database models.
- Implement `from_mongo` class methods in response models to convert MongoEngine documents to Pydantic models.
- Use appropriate field types and validation in MongoEngine models.

## API Integrations
- Store API keys and sensitive information in environment variables.
- Implement robust error handling for external API calls.
- Use asynchronous programming techniques for API requests.

## Testing
- Use pytest for Python tests.
