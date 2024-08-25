# FastAPI MongoDB Project

## Overview
This project is a FastAPI-based web application that integrates with MongoDB. It provides a RESTful API for managing various resources, including campaigns, companies, contacts, emails, and users.

## Features
- FastAPI framework for high-performance API development
- MongoDB integration using MongoEngine ODM
- JWT-based authentication
- CORS middleware for cross-origin resource sharing
- Environment variable configuration using python-dotenv

## Prerequisites
- Python 3.7+
- MongoDB

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the project root and add the following variables:
   ```
   MONGODB_URI=<your-mongodb-uri>
   SECRET_KEY=<your-secret-key>
   ```

## Running the Application

To run the application, use the following command:

```
python main.py
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

- `main.py`: The main entry point of the application
- `config.py`: Configuration settings for the project
- `api/v1/`: API version 1 routes and endpoints
- `models/`: MongoDB document models
- `requirements.txt`: List of project dependencies

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
