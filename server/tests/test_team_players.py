from models.datatypes import Teams, Positions

BASEURL = "/leagues/1/teams/1/players"


async def test_adding_player(auth_client_players):
    response = await auth_client_players.post(BASEURL, json={"id": 15})

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "NYG"
    assert data["position"] == Positions.DST
    assert data["team"] == Teams.NYG
    assert data["points_ppr"] == 9.0


async def test_adding_wrong_player(auth_client_players):
    response = await auth_client_players.post(BASEURL, json={"id": 99999})

    assert response.status_code == 404


async def test_adding_player_to_wrong_team(auth_client_players):
    response = await auth_client_players.post(
        "/leagues/1/teams/999/players", json={"id": 15}
    )

    assert response.status_code == 404


async def test_adding_player_to_wrong_team_league(auth_client_players):
    response = await auth_client_players.post(
        "/leagues/999/teams/1/players", json={"id": 15}
    )

    assert response.status_code == 404


async def test_no_auth_add_player(auth_client_players):
    response = await auth_client_players.noauth_post(BASEURL, json={"id": 15})

    assert response.status_code == 401


async def test_add_player_wrong_payload(auth_client_players):
    response = await auth_client_players.post(BASEURL, json={"wrong": 15})

    assert response.status_code == 422


async def test_add_same_player_two_teams(auth_client_players):
    await auth_client_players.post(BASEURL, json={"id": 15})

    response = await auth_client_players.post(
        "/leagues/1/teams/2/players", json={"id": 15}
    )

    assert response.status_code == 400


async def test_get_players(auth_client_trade):
    response = await auth_client_trade.get(BASEURL)

    assert response.status_code == 200

    data = response.json()["players"]

    assert len(data) == 8
    player_names = [p["name"] for p in data]
    assert "Jaxson Dart" in player_names


async def test_get_players_wrong_league(auth_client_trade):
    response = await auth_client_trade.get("leagues/999/teams/1/players")

    assert response.status_code == 404


async def test_get_players_wrong_team(auth_client_trade):
    response = await auth_client_trade.get("leagues/1/teams/999/players")

    assert response.status_code == 404


async def test_get_players_no_initialised_players(auth_client_players):
    response = await auth_client_players.get(BASEURL)

    assert response.status_code == 200

    assert len(response.json()["players"]) == 0


async def test_no_auth_get_players(auth_client_trade):
    response = await auth_client_trade.noauth_get(BASEURL)

    assert response.status_code == 401


DELETEURL = f"{BASEURL}/1"


async def test_delete_player(auth_client_trade):
    response = await auth_client_trade.get(BASEURL)

    assert response.status_code == 200

    data = response.json()["players"]
    player_names = [p["name"] for p in data]

    assert "Josh Allen" in player_names

    await auth_client_trade.delete(DELETEURL)

    updated = await auth_client_trade.get(BASEURL)
    updated_data = updated.json()["players"]

    assert len(updated_data) == len(data) - 1
    updated_player_names = [p["name"] for p in updated_data]

    assert "Josh Allen" not in updated_player_names


async def test_delete_player_no_auth(auth_client_trade):
    response = await auth_client_trade.noauth_delete(DELETEURL)

    assert response.status_code == 401


async def test_delete_player_wrong_player_id(auth_client_trade):
    response = await auth_client_trade.delete("/leagues/1/teams/1/players/999")

    assert response.status_code == 404


async def test_delete_player_wrong_league_id(auth_client_trade):
    response = await auth_client_trade.delete("/leagues/999/teams/1/players/9199")

    assert response.status_code == 404


async def test_delete_player_wrong_team_id(auth_client_trade):
    response = await auth_client_trade.delete("/leagues/1/teams/999/players/1")

    assert response.status_code == 404
