import pytest
import sys
import os
from fastapi.testclient import TestClient
from httpx import ASGITransport
from mongoengine import connect, disconnect
import mongomock

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from main import app

@pytest.fixture(scope="function")
def client():
    # Set up
    disconnect()
    connect('mongoenginetest', mongo_client_class=mongomock.MongoClient)
    
    # Create a test client using the FastAPI app
    test_client = TestClient(app, transport=ASGITransport(app=app))
    
    yield test_client
    
    # Tear down
    disconnect()
