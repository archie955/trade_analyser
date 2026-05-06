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
    def __init__(self, client, user, db=None) -> None:
        self.client = client
        self.db = db
        self.user = user
    
    async def seed_leagues(self) -> None:
        league = League(id=1, user_id=1, name="Trade League")
        alt_league = League(id=2, user_id=1, name="Alt League")
        self.db.add_all([league, alt_league])
        await self.db.flush()

    async def seed_teams(self) -> None:
        team1 = Team(
            id=1,
            name="Trade Team",
            user_id=1,
            league_id=1
        )

        team2 = Team(
            id=2,
            name="Alt Team",
            user_id=1,
            league_id=1
        )

        self.db.add_all([team1, team2])
        await self.db.flush()

    async def seed_players(self) -> None:
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
            await self.db.flush()

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
            await self.db.flush()

    async def seed_players_teams(self, team1_id, team2_id) -> None:
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
            await self.db.flush()

            self.db.add(
                TeamPlayer(team_id=team1_id, league_id=1, player_id=player.id)
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
            await self.db.flush()

            self.db.add(
                TeamPlayer(team_id=team2_id, league_id=1, player_id=player.id)
            )
        
        await self.db.flush()

    def auth_headers(self, expired=False) -> dict:
        token = self.user["access_token"]
        if expired:
            token = "expired_token"
        return {
            "Authorization": f"Bearer {token}"
        }

    async def request(self, method, url, **kwargs):
        headers = kwargs.pop("headers", {})
        headers.update(self.auth_headers())
        response = await self.client.request(method, url, headers=headers, **kwargs)
        return response
    
    async def get(self, url, **kwargs):
        response = await self.request("GET", url, **kwargs)
        return response
    
    async def post(self, url, **kwargs):
        response = await self.request("POST", url, **kwargs)
        return response
    
    async def put(self, url, **kwargs):
        response = await self.request("PUT", url, **kwargs)
        return response
    
    async def delete(self, url, **kwargs):
        response = await self.request("DELETE", url, **kwargs)
        return response
    
    async def noauth_get(self, url, **kwargs):
        response = await self.client.get(url, **kwargs)
        return response
    
    async def noauth_post(self, url, **kwargs):
        response = await self.client.post(url, **kwargs)
        return response
    
    async def noauth_put(self, url, **kwargs):
        response = await self.client.put(url, **kwargs)
        return response
    
    async def noauth_delete(self, url, **kwargs):
        response = await self.client.delete(url, **kwargs)
        return response

@pytest_asyncio.fixture
async def auth_client(client, helpers):
    user = await helpers.full_login(client)
    
    return AuthClient(client, user)

@pytest_asyncio.fixture
async def auth_client_leagues(client, db, helpers):
    user = await helpers.full_login(client)
    ac = AuthClient(client, user, db=db)
    await ac.seed_leagues()

    return ac

@pytest_asyncio.fixture
async def auth_client_teams(client, db, helpers):
    user = await helpers.full_login(client)
    ac = AuthClient(client, user, db=db)
    await ac.seed_leagues()
    await ac.seed_teams()

    return ac

@pytest_asyncio.fixture
async def auth_client_players(client, db, helpers):
    user = await helpers.full_login(client)

    ac = AuthClient(client, user, db=db)
    await ac.seed_leagues()
    await ac.seed_teams()
    await ac.seed_players()

    return ac

@pytest_asyncio.fixture
async def auth_client_trade(client, db, helpers):
    user = await helpers.full_login(client)
    
    ac = AuthClient(client, user, db=db)
    await ac.seed_leagues()
    await ac.seed_teams()
    await ac.seed_players_teams(1, 2)

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
            "/users",
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
            "/users",
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
            "/users",
            json=updated,
            headers={"Authorization": f"Bearer {user['access_token']}"}
            )

        assert response.status_code == 200
        return response.json()
    
@pytest_asyncio.fixture
def helpers():
    return Helpers
