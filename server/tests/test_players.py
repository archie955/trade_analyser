from models.datatypes import Teams, Positions
from tests.rawdata import data

BASEURL = "/players/1/1"
LENGTH = len(data["team1"]) + len(data["team2"])


async def test_get_players(auth_client_team_players):
    response = await auth_client_team_players.get(BASEURL)

    assert response.status_code == 200

    players = response.json()["players"]
    assert len(players) == LENGTH - 4
    assert players[0]["name"] == "Jaxson Dart"
    assert players[0]["team_id"] is None


async def test_get_players_asc(auth_client_team_players):
    response = await auth_client_team_players.get(f"{BASEURL}?asc=True")

    assert response.status_code == 200

    players = response.json()["players"]
    assert len(players) == LENGTH - 4
    assert players[0]["name"] == "Graham Gano"
    assert players[0]["team_id"] is None
    assert players[0]["points_ppr"] == 3.9


async def test_get_players_limit(auth_client_team_players):
    response = await auth_client_team_players.get(f"{BASEURL}?limit=3")

    assert response.status_code == 200

    players = response.json()["players"]
    assert len(players) == 3


async def test_get_players_skip(auth_client_team_players):
    response = await auth_client_team_players.get(f"{BASEURL}?skip=3")

    assert response.status_code == 200

    players = response.json()["players"]
    assert len(players) == LENGTH - 7
    assert players[0]["name"] == "Tyler Warren"
    assert players[0]["team_id"] == 2


async def test_get_players_position(auth_client_team_players):
    response = await auth_client_team_players.get(f"{BASEURL}?pos=QB")

    assert response.status_code == 200

    players = response.json()["players"]
    assert len(players) == 3
    for player in players:
        assert player["position"] == Positions.QB


async def test_get_players_team(auth_client_team_players):
    response = await auth_client_team_players.get(f"{BASEURL}?team=NYG")

    assert response.status_code == 200

    players = response.json()["players"]
    assert len(players) == 4
    for player in players:
        assert player["team"] == Teams.NYG


async def test_get_players_free_agent(auth_client_team_players):
    response = await auth_client_team_players.get(f"{BASEURL}?free_agent=True")

    assert response.status_code == 200

    players = response.json()["players"]

    assert len(players) == LENGTH - 8
    assert players[0]["name"] == "Jaxson Dart"


async def test_get_players_multiple_params(auth_client_team_players):
    response = await auth_client_team_players.get(
        f"{BASEURL}?team=NYG&free_agent=True&asc=True"
    )

    assert response.status_code == 200

    players = response.json()["players"]

    assert len(players) == 2
    assert players[0]["name"] == "Graham Gano"
    assert players[1]["name"] == "Jaxson Dart"


async def test_get_players_wrong_datatype_param(auth_client_team_players):
    response = await auth_client_team_players.get(f"{BASEURL}?limit=False")

    assert response.status_code == 422


async def test_get_players_wrong_datatype_enum(auth_client_team_players):
    response = await auth_client_team_players.get(f"{BASEURL}?pos=FLEX")

    assert response.status_code == 422


async def test_get_players_wrong_league_id(auth_client_team_players):
    response = await auth_client_team_players.get("/players/444/1")

    assert response.status_code == 404

async def test_get_players_wrong_team_id(auth_client_team_players):
    response = await auth_client_team_players.get("/players/1/444")

    assert response.status_code == 404

async def test_get_players_no_current_team_players(auth_client_team_players):
    response = await auth_client_team_players.get(f"{BASEURL}")

    assert response.status_code == 200

    player_names = [p["name"] for p in response.json()["players"]]

    assert "Josh Allen" not in player_names

    response_2 = await auth_client_team_players.get("/players/1/2")

    assert response.status_code == 200

    player_names_2 = [p["name"] for p in response_2.json()["players"]]

    assert "Josh Allen" in player_names_2
    