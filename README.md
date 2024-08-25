# Sales Manager Project

## Overview
The Sales Manager Project consists of a FastAPI-based backend API and an Angular frontend. The backend provides a RESTful API for managing various resources, including campaigns, companies, contacts, emails, and users, while the frontend offers a user-friendly interface for interacting with these resources.

## Features
- FastAPI framework for high-performance API development
- MongoDB integration using MongoEngine ODM
- JWT-based authentication
- CORS middleware for cross-origin resource sharing
- Environment variable configuration using python-dotenv
- Pydantic settings management

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

## Configuration

The project uses a `config.py` file to manage settings. You can modify the following settings:

- `PROJECT_NAME`: Name of the project
- `PROJECT_VERSION`: Version of the project
- `API_V1_STR`: API version 1 prefix
- `MONGODB_URI`: MongoDB Atlas connection string
- `DATABASE_NAME`: Name of the MongoDB database
- `SECRET_KEY`: Secret key for JWT encoding/decoding
- `ALGORITHM`: Algorithm used for JWT
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Expiration time for access tokens
- `ALLOWED_HOSTS`: List of allowed hosts for CORS

## MongoDB Atlas Setup

1. Create a MongoDB Atlas account if you don't have one.
2. Set up a new cluster and obtain the connection string.
3. In your `.env` file, set the `MONGODB_URI` to your Atlas connection string:
   ```
   MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/<dbname>?retryWrites=true&w=majority
   DATABASE_NAME=your_database_name
   ```

## Running the Application

### Backend

To run the backend application, use the following command:

```
cd backend
python main.py
```

The API will be available at `http://localhost:8000`.

Note: Ensure that your IP address is whitelisted in the MongoDB Atlas network access settings.

### Frontend

To run the frontend application, use the following commands:

```
cd frontend/sales-manager-ui
ng serve
```

The Angular app will be available at `http://localhost:4200`.

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Health Check

The application includes a health check endpoint to verify the database connection:

```
GET /health
```

This endpoint returns:
- `{"status": "healthy", "database": "connected"}` if the database is connected
- A 503 error if the database is not available

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
