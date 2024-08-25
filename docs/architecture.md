# Project Architecture Guidelines

This document outlines the architectural rules and guidelines that both AI assistants and developers should follow when working on this project.

## 1. Project Structure

- The project follows a modular structure with clear separation of concerns.
- Main components:
  - `api/`: Contains API-related code
  - `models/`: Contains data models
  - `docs/`: Contains project documentation
  - `tests/`: Contains test files

## 2. API Structure

- The API is versioned (e.g., `api/v1/`).
- Endpoints are organized by resource type (e.g., `users`, `campaigns`, `contacts`, `companies`, `emails`).
- Each resource has its own router in a separate file within the `api/v1/endpoints/` directory.

## 3. Models

- Data models are defined using MongoEngine for database interactions.
- Pydantic models are used for request/response schemas.
- Each model has its own file in the `models/` directory.
- Models should include:
  - MongoEngine Document class
  - Pydantic BaseModel classes for Create, Response, and Update operations

## 4. Logging

- Comprehensive logging is implemented across all endpoints.
- Use the `logging` module for consistent log formatting.
- Log levels:
  - INFO: Successful operations
  - WARNING: Not found resources
  - ERROR: Validation errors and unexpected exceptions
- Include `exc_info=True` for full stack traces on unexpected exceptions.

## 5. Error Handling

- Use FastAPI's `HTTPException` for raising HTTP errors.
- Catch and handle specific exceptions (e.g., `ValidationError`, `DoesNotExist`).
- Provide meaningful error messages in the response.

## 6. Code Style

- Follow PEP 8 guidelines for Python code style.
- Use type hints for function parameters and return values.
- Use docstrings to document classes and functions.

## 7. API Endpoints

- Use appropriate HTTP methods (GET, POST, PUT, DELETE) for CRUD operations.
- Implement pagination for list endpoints using `skip` and `limit` query parameters.
- Use Pydantic models for request body validation and response serialization.

## 8. Database Operations

- Use MongoEngine for database interactions.
- Perform database operations within try-except blocks to handle potential errors.
- Use appropriate MongoEngine methods for querying and updating documents.

## 9. Configuration

- Store configuration variables in a separate `config.py` file.
- Use environment variables for sensitive information.

## 10. Testing

- Write unit tests for all API endpoints and models.
- Use pytest as the testing framework.
- Organize tests in the `tests/` directory, mirroring the project structure.

## 11. Documentation

- Maintain up-to-date documentation in the `docs/` directory.
- Include README.md files in each major directory to explain its purpose and contents.

## 12. Versioning

- Use semantic versioning for the project.
- Maintain a CHANGELOG.md file to track changes between versions.

## 13. Dependencies

- Keep track of project dependencies in a `requirements.txt` file.
- Regularly update dependencies and check for security vulnerabilities.

By following these guidelines, we ensure consistency, maintainability, and scalability of the project as it grows and evolves.
