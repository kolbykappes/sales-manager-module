# Sales Manager Project Coding Guidelines

## General
- Follow PEP 8 style guide for Python code.
- Use meaningful and descriptive names for variables, functions, and classes.
- Write docstrings for classes and functions.
- Implement error handling and logging throughout the application.
- Use type hints in function signatures and variable declarations.

## Backend (FastAPI)
- Organize endpoints into separate files under `api/v1/endpoints/`.
- Use Pydantic models for request/response schemas.
- Implement proper input validation using Pydantic models.
- Use async functions for database operations and external API calls.
- Implement proper error handling and use FastAPI's HTTPException for API errors.

## Database (MongoDB with MongoEngine)
- Define document models in separate files under the `models/` directory.
- Use MongoEngine's Document class for defining database models.
- Implement `from_mongo` class methods in response models to convert MongoEngine documents to Pydantic models.
- Use appropriate field types and validation in MongoEngine models.

## Frontend (Angular)
- Use Angular's standalone components.
- Organize components, services, and models into appropriate directories.
- Use Angular's built-in pipes for data transformation in templates.
- Implement proper error handling and display user-friendly messages.
- Use Angular's HttpClient for API calls.

## API Integrations
- Store API keys and sensitive information in environment variables.
- Implement robust error handling for external API calls.
- Use asynchronous programming techniques for API requests.

## Security
- Use parameterized queries to prevent injection attacks.
- Implement proper authentication and authorization mechanisms.
- Hash passwords before storing them in the database.
- Use HTTPS for all communications in production.

## Testing
- Write unit tests for backend logic and API endpoints.
- Use pytest for Python tests.
- Implement integration tests for critical workflows.
- Use mock objects for external dependencies in tests.

## Configuration
- Use a `config.py` file with a `Settings` class for application configuration.
- Utilize environment variables for sensitive information and deployment-specific settings.

## Documentation
- Maintain up-to-date API documentation.
- Document complex business logic and important architectural decisions.
- Use clear and concise comments for non-obvious code sections.

## Version Control
- Use meaningful commit messages.
- Create feature branches for new developments.
- Perform code reviews before merging into the main branch.

Remember to balance between code quality, performance, and development speed when making implementation decisions. Regularly review and update these guidelines as the project evolves.
