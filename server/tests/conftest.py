import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from main import app
from database.database import get_db
from models.models import Base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5433/test_db" # just a test database that gets made for tests then dropped immediately


@pytest.fixture(scope="function")
def engine():
    engine = create_engine(url=SQLALCHEMY_DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    yield db
    db.close()

@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()

@pytest.fixture
def authenticated_user(client):
    user = {
        "email": "authuser@example.com",
        "username": "authusername",
        "password": "authpassword"
    }

    user_in_db = client.post("/users/", json=user).json()

    response = client.post("/users/login",
                           data={
                               "username": user["email"],
                               "password": user["password"]
                           },
                           headers={"Content-Type": "application/x-www-form-urlencoded"}
                        )
    access_token = response.json()["access_token"]

    return {
        "email": user_in_db["email"],
        "username": user_in_db["username"],
        "password": user["password"],
        "created_at": user_in_db["created_at"],
        "updated_at": user_in_db["updated_at"],
        "access_token": access_token
    }

class Helpers:
    def auth_headers(authenticated_user):
        return {
            "Authorization": f"Bearer {authenticated_user['access_token']}"
        }
    
    def register_user(client):
        response = client.post(
            "/users/",
            json={
                "email": "authuser@example.com",
                "username": "authusername",
                "password": "authpassword"
            }
        )

        assert response.status_code == 201
        return response.json()
    
@pytest.fixture
def helpers():
    return Helpers()