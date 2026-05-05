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