# Project Coding Guidelines

## General
- Use meaningful and descriptive names for variables, functions, and classes.
- Follow the DRY (Don't Repeat Yourself) principle to minimize code duplication.
- Write unit tests for all new functionality to ensure code reliability.
- Use consistent code formatting and adhere to PEP 8 style guide for Python code.
- Document complex logic and public APIs.

## PyQt6 UI Development
- Create modular UI components for better maintainability.
- Use Qt Designer for complex layouts, export to .ui files, and convert to Python code.
- Implement proper signal-slot connections for event handling.
- Use QThreads or QRunners for long-running tasks to keep the UI responsive.

## API Integrations (OpenAI GPT-4 and ZoomInfo)
- Use environment variables for API keys and sensitive information.
- Implement robust error handling and logging for API calls.
- Use asynchronous programming techniques for API requests when appropriate.
- Implement rate limiting and respect API usage guidelines.

## MongoDB Atlas Integration
- Use PyMongo for database operations.
- Implement proper connection pooling and error handling for database operations.
- Use appropriate indexing for frequently queried fields.

## Security
- Always use parameterized queries to prevent injection attacks.
- Implement proper input validation on both UI and backend.
- Use secure methods for storing and managing API credentials.
- Implement proper authentication and authorization mechanisms if required.

## Performance and Scalability
- Optimize database queries and use appropriate indexing.
- Implement caching strategies where applicable.
- Use efficient data structures and algorithms, especially for email generation and campaign management.

## Error Handling and Logging
- Implement comprehensive error handling throughout the application.
- Use Python's logging module for consistent log formatting.
- Provide user-friendly error messages in the UI.

Remember to always consider the trade-offs between performance, maintainability, and development speed when making implementation decisions.