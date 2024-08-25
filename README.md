# Sales Manager Project

## Overview
The Sales Manager Project consists of a FastAPI-based backend API and an Angular frontend. The backend provides a RESTful API for managing various resources, including campaigns, companies, contacts, emails, and users, while the frontend offers a user-friendly interface for interacting with these resources.

## Backend Features
- FastAPI framework for high-performance API development
- MongoDB integration using MongoEngine ODM
- JWT-based authentication
- CORS middleware for cross-origin resource sharing
- Environment variable configuration using python-dotenv
- Pydantic settings management

## Frontend Features
- Angular framework for building dynamic web applications
- Modular architecture for scalability and maintainability
- Integration with backend API using HttpClient
- Reactive forms for user input handling
- Angular Material for consistent UI components

## Prerequisites
- Python 3.7+
- MongoDB
- Node.js and npm

## Installation

### Backend

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

### Frontend

1. Navigate to the frontend directory:
   ```
   cd frontend/sales-manager-ui
   ```

2. Install dependencies:
   ```
   npm install
   ```

## Running the Application

### Backend

To run the backend application, use the following command:

```
python main.py
```

The API will be available at `http://localhost:8000`.

### Frontend

To run the frontend application, use the following command:

```
ng serve
```

The Angular app will be available at `http://localhost:4200`.

## API Documentation

Once the backend is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Project Structure

- `main.py`: The main entry point of the backend application
- `config.py`: Configuration settings for the project
- `api/v1/`: API version 1 routes and endpoints
- `models/`: MongoDB document models
- `frontend/sales-manager-ui/`: Angular frontend application

## Contributing

Please read CONTRIBUTING.md for details on our code of conduct, and the process for submitting pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
