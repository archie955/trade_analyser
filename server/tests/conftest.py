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
    db.rollback()
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

class AuthClient:
    def __init__(self, client, user, leagues=False):
        self.client = client
        self.user = user
        if leagues:
            self.post("/leagues/", json={"name": "league_1"})
            self.post("/leagues/", json={"name": "league_2"})

    def auth_headers(self, expired=False):
        token = self.user["access_token"]
        if expired:
            token = "expired_token"
        return {
            "Authorization": f"Bearer {token}"
        }

    def request(self, method, url, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update(self.auth_headers())
        return self.client.request(method, url, headers=headers, **kwargs)
    
    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)
    
    def post(self, url, **kwargs):
        print(f"posting to {url} with kwargs {kwargs}")
        return self.request("POST", url, **kwargs)
    
    def put(self, url, **kwargs):
        return self.request("PUT", url, **kwargs)
    
    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)
    
    def noauth_get(self, url, **kwargs):
        return self.client.get(url, **kwargs)
    
    def noauth_post(self, url, **kwargs):
        return self.client.post(url, **kwargs)
    
    def noauth_put(self, url, **kwargs):
        return self.client.put(url, **kwargs)
    
    def noauth_delete(self, url, **kwargs):
        return self.client.delete(url, **kwargs)

@pytest.fixture
def auth_client(client, helpers):
    user = helpers.full_login(client)
    
    return AuthClient(client, user)

@pytest.fixture
def auth_client_leagues(client, helpers):
    user = helpers.full_login(client)

    return AuthClient(client, user, leagues=True)

class Helpers:
    @staticmethod
    def register_user(client):
        user = {
            "email": "authuser@example.com",
            "username": "authusername",
            "password": "authpassword"
        }
        response = client.post(
            "/users/",
            json=user
        )

        assert response.status_code == 201
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data
        return user
    
    @staticmethod
    def full_login(client):
        user = {
            "email": "authuser@example.com",
            "username": "authusername",
            "password": "authpassword"
        }
        user_payload = client.post(
            "/users/",
            json=user
        )

        assert user_payload.status_code == 201

        response = client.post(
            "/users/login",
            data={
                "username": user["email"],
                "password": user["password"]
            },
            headers={
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        user["access_token"] = data["access_token"]
        return user
    
    @staticmethod
    def auth_headers(user, expired=False):
        token = user["access_token"]
        if expired:
            token = "expired_token"
        return {
            "Authorization": f"Bearer {token}"
        }
    
    @staticmethod
    def update_user(client, updated, user):
        response = client.put(
            "/users/",
            json=updated,
            headers={"Authorization": f"Bearer {user['access_token']}"}
            )

        assert response.status_code == 200
        return response.json()
    
@pytest.fixture
def helpers():
    return Helpers
