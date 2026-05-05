from models.datatypes import Teams, Positions

async def test_adding_player(auth_client_players):
    response = await auth_client_players.post(
        "/leagues/1/teams/1/players/",
        json={"id": 15}
    )

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "NYG"
    assert data["position"] == Positions.DST
    assert data["team"] == Teams.NYG
    assert data["points_ppr"] == 9.0