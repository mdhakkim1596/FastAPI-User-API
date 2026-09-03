# from dotenv import load_dotenv
# load_dotenv()
import os
os.environ.setdefault("SECRET_KEY", "test-secret-key")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from main import app
from database.connection import Base, get_db

TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def get_token():
    client.post(
        "/users",
        json={
            "name": "Auth User",
            "email": "authuser@gmail.com",
            "age": 25,
            "phone_number": "+919876543021",
            "gender": "Male",
            "password": "Testuser@123",
            "confirm_password": "Testuser@123",
        },
    )
    response = client.post(
        "/auth/login", json={"email": "authuser@gmail.com", "password": "Testuser@123"}
    )
    return response.json()["access_token"]
