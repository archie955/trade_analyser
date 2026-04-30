import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from main import app
from database.database import get_db
from models.models import Base, League, Team, Player, TeamPlayer
from tests.rawdata import data

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5433/test_db" # just a test database that gets made for tests then dropped immediately

@pytest_asyncio.fixture(scope="function")
async def engine():
    engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db(engine):
    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with SessionLocal() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture(scope="function")
async def client(db):
    async def override_get_db():
        yield db
    
    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test"
    ) as client:
        yield client

    app.dependency_overrides.clear()

class AuthClient:
    def __init__(self, client, user, db=None, leagues=False, teams=False):
        self.client = client
        self.db = db
        self.user = user
        if leagues:
            self.post("/leagues/", json={"name": "league_1"})
            self.post("/leagues/", json={"name": "league_2"})

        if leagues and teams:
            self.post("/teams/1", json={"name": "team_1"})
            self.post("/teams/1", json={"name": "team_2"})

    def seed_trade_setup(self):
        league = League(user_id=1, name="Trade League")
        self.db.add(league)
        self.db.flush()
        
        team1 = Team(
            name="team_1",
            user_id=1,
            league_id=league.id
        )

        team2 = Team(
            name="team_2",
            user_id=1,
            league_id=league.id
        )

        self.db.add_all([team1, team2])
        self.db.flush()

        self.seed_players(team1.id, team2.id)

        self.db.commit()

        return {
            "league_id": league.id,
            "team1_id": team1.id,
            "team2_id": team2.id
        }
    
    def seed_players(self, team1_id, team2_id):
        for p in data["team1"]:
            player = Player(
                id=p["id"],
                name=p["name"],
                team=p["team"],
                position=p["position"],
                points_ppr=p["points"],
                points_halfppr=p["points"],
                points_noppr=p["points"],
            )
            self.db.add(player)
            self.db.flush()

            self.db.add(
                TeamPlayer(team_id=team1_id, player_id=player.id)
            )

        for p in data["team2"]:
            player = Player(
                id=p["id"],
                name=p["name"],
                team=p["team"],
                position=p["position"],
                points_ppr=p["points"],
                points_halfppr=p["points"],
                points_noppr=p["points"],
            )
            self.db.add(player)
            self.db.flush()

            self.db.add(
                TeamPlayer(team_id=team2_id, player_id=player.id)
            )


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

@pytest_asyncio.fixture
def auth_client(client, helpers):
    user = helpers.full_login(client)
    
    return AuthClient(client, user)

@pytest_asyncio.fixture
def auth_client_leagues(client, helpers):
    user = helpers.full_login(client)

    return AuthClient(client, user, leagues=True)

@pytest_asyncio.fixture
def auth_client_teams(client, helpers):
    user = helpers.full_login(client)

    return AuthClient(client, user, leagues=True, teams=True)

@pytest_asyncio.fixture
def auth_client_trade(client, db, helpers):
    user = helpers.full_login(client)

    ac = AuthClient(client, user, db=db)
    ac.seed_trade_setup()

    return ac

class Helpers:
    @staticmethod
    async def register_user(client: AsyncClient) -> dict:
        user = {
            "email": "authuser@example.com",
            "username": "authusername",
            "password": "authpassword"
        }
        response = await client.post(
            "/users/",
            json=user
        )

        assert response.status_code == 201
        data = response.json()
        assert "created_at" in data
        assert "updated_at" in data
        return user
    
    @staticmethod
    async def full_login(client: AsyncClient) -> dict:
        user = {
            "email": "authuser@example.com",
            "username": "authusername",
            "password": "authpassword"
        }
        user_payload = await client.post(
            "/users/",
            json=user
        )

        assert user_payload.status_code == 201

        response = await client.post(
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
    async def update_user(client, updated, user):
        response = await client.put(
            "/users/",
            json=updated,
            headers={"Authorization": f"Bearer {user['access_token']}"}
            )

        assert response.status_code == 200
        return response.json()
    
@pytest_asyncio.fixture
def helpers():
    return Helpers
