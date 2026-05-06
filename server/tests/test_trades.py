async def test_trade_endpoint(auth_client_trade):
    response = await auth_client_trade.get("/leagues/1/teams/1/trade")

    assert response.status_code == 200

    data = response.json()
    print(data)
    assert data["Alt Team"] == [
        {'players_1': [{'id': 1, 'name': 'Josh Allen'}], 'gain_1': 5.5, 'players_2': [{'id': 6, 'name': 'Tyler Warren'}], 'gain_2': 5.299999999999997},
        {'players_1': [{'id': 1, 'name': 'Josh Allen'}], 'gain_1': 3.5, 'players_2': [{'id': 15, 'name': 'NYG'}], 'gain_2': 5.299999999999997},
        {'players_1': [{'id': 9, 'name': 'Brandon Aubrey'}], 'gain_1': 5.0, 'players_2': [{'id': 6, 'name': 'Tyler Warren'}], 'gain_2': 3.0},
        {'players_1': [{'id': 9, 'name': 'Brandon Aubrey'}], 'gain_1': 3.0, 'players_2': [{'id': 15, 'name': 'NYG'}], 'gain_2': 3.0},
        {'players_1': [{'id': 1, 'name': 'Josh Allen'}, {'id': 9, 'name': 'Brandon Aubrey'}], 'gain_1': 8.5, 'players_2': [{'id': 6, 'name': 'Tyler Warren'}, {'id': 15, 'name': 'NYG'}], 'gain_2': 8.299999999999997}
        ]
    
async def test_trade_no_auth(auth_client_trade):
    response = await auth_client_trade.noauth_get("/leagues/1/teams/1/trade")

    assert response.status_code == 401

async def test_trade_wrong_team_id(auth_client_trade):
    response = await auth_client_trade.get("/leagues/1/teams/999/trade")

    assert response.status_code == 404

async def test_trade_wrong_league_id(auth_client_trade):
    response = await auth_client_trade.get("/leagues/999/teams/1/trade")

    assert response.status_code == 404

async def test_trade_no_players(auth_client_teams):
    response = await auth_client_teams.get("/leagues/1/teams/1/trade")

    assert response.status_code == 404

async def test_trade_only_one_team(auth_client_trade):
    await auth_client_trade.delete("/leagues/1/teams/2")

    response = await auth_client_trade.get("/leagues/1/teams/1/trade")

    assert response.status_code == 400

async def test_trade_only_one_team_has_players(auth_client_players):
    await auth_client_players.post(
        "/leagues/1/teams/1/players",
        json={"id": 1}
    )

    response = await auth_client_players.get("/leagues/1/teams/1/trade")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 0
    