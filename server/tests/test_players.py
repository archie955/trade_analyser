from models.datatypes import Teams, Positions

BASEURL = "/players/1"

async def test_get_players(auth_client_players):
    response = await auth_client_players.get(BASEURL)

    print(response.json())

    assert response.status_code == 201