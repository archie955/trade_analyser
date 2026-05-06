async def test_trade_endpoint(auth_client_trade):
    response = await auth_client_trade.get("/leagues/1/teams/1/trade")

    assert response.status_code == 200

    data = response.json()
    assert data["Alt Team"] == [
        {'team1_players': [[1, 'Josh Allen']], 'team2_players': [[6, 'Tyler Warren']], 'team1_gain': 5.5, 'team2_gain': 5.299999999999997},
        {'team1_players': [[1, 'Josh Allen']], 'team2_players': [[15, 'NYG']], 'team1_gain': 3.5, 'team2_gain': 5.299999999999997},
        {'team1_players': [[9, 'Brandon Aubrey']], 'team2_players': [[6, 'Tyler Warren']], 'team1_gain': 5.0, 'team2_gain': 3.0},
        {'team1_players': [[9, 'Brandon Aubrey']], 'team2_players': [[15, 'NYG']], 'team1_gain': 3.0, 'team2_gain': 3.0},
        {'team1_players': [[1, 'Josh Allen'], [9, 'Brandon Aubrey']], 'team2_players': [[6, 'Tyler Warren'], [15, 'NYG']], 'team1_gain': 8.5, 'team2_gain': 8.299999999999997}
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
    