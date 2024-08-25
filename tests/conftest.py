import pytest
from fastapi.testclient import TestClient
from mongoengine import connect, disconnect
from main import app

@pytest.fixture(scope="function")
def client():
    # Set up
    disconnect()
    connect('mongoenginetest', host='mongomock://localhost')
    
    # Create a test client using the FastAPI app
    test_client = TestClient(app)
    
    yield test_client
    
    # Tear down
    disconnect()
