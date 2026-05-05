async def test_create_team(auth_client_leagues):
    response = await auth_client_leagues.post(
        "/leagues/1/teams",
        json={"name": "team_1"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "team_1"
    assert data["league_id"] == 1
    assert "created_at" in data
    assert "id" in data
    assert "updated_at" in data

async def test_no_auth_create_team(auth_client_leagues):
    response = await auth_client_leagues.noauth_post(
        "/leagues/1/teams",
        json={"name": "testteamnoauth"}
    )

    assert response.status_code == 401

async def test_create_team_wrong_payload(auth_client_leagues):
    response = await auth_client_leagues.post(
        "/leagues/1/teams",
        json={"wrong": "testteam"}
    )

    assert response.status_code == 422

async def test_create_team_same_name(auth_client_teams):
    response = await auth_client_teams.post(
        "/leagues/1/teams",
        json={"name": "Trade Team"}
    )

    assert response.status_code == 400

async def test_get_teams(auth_client_teams):
    response = await auth_client_teams.get(
        "/leagues/1/teams"
    )

    assert response.status_code == 200

    data = response.json()["teams"]

    assert len(data) == 2
    
    for t in data:
        if t["id"] == 1:
            team = t
            break
        else:
            team = None
    assert team["name"] == "Trade Team"
    assert team["league_id"] == 1
    assert "created_at" in team
    assert "id" in team
    assert "updated_at" in team 

async def test_get_teams_no_auth(auth_client_teams):
    response = await auth_client_teams.noauth_get(
        "/leagues/1/teams"
    )

    assert response.status_code == 401

async def test_get_no_teams(auth_client_leagues):
    response = await auth_client_leagues.get(
        "/leagues/1/teams"
    )

    assert response.status_code == 200
    data = response.json()["teams"]

    assert len(data) == 0

async def test_update_team(auth_client_teams):
    team_to_update = (await auth_client_teams.get(
        "/leagues/1/teams"
    )).json()["teams"][0]

    updated = {"id": team_to_update["id"], "name": "newname"}

    response = await auth_client_teams.put(
        "/leagues/1/teams",
        json=updated
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "newname"
    assert data["league_id"] == 1
    assert "created_at" in data
    assert "id" in data
    assert "updated_at" in data

async def test_update_team_missing_name(auth_client_teams):
    team_to_update = (await auth_client_teams.get(
        "/leagues/1/teams"
    )).json()["teams"][0]

    updated = {"id": team_to_update["id"]}

    response = await auth_client_teams.put(
        "/leagues/1/teams",
        json=updated
    )

    assert response.status_code == 422

async def test_update_team_wrong_id(auth_client_teams):
    updated = {"id": 9999, "name": "newname"}

    response = await auth_client_teams.put(
        "/leagues/1/teams",
        json=updated
    )

    assert response.status_code == 404

async def test_update_team_not_auth(auth_client_teams):
    team_to_update = (await auth_client_teams.get(
        "/leagues/1/teams"
    )).json()["teams"][0]

    updated = {"id": team_to_update["id"], "name": "newname"}

    response = await auth_client_teams.noauth_put(
        "/leagues/1/teams",
        json=updated
    )

    assert response.status_code == 401

async def test_delete_team(auth_client_teams):
    teams = (await auth_client_teams.get(
        "/leagues/1/teams"
    )).json()["teams"]

    team_to_delete = teams[0]

    id = team_to_delete["id"]

    response = await auth_client_teams.delete(
        f"/leagues/1/teams/{id}"
    )

    assert response.status_code == 204

    updated_teams = (await auth_client_teams.get(
        "/leagues/1/teams"
    )).json()["teams"]

    assert len(updated_teams) == len(teams) - 1

    ids = set(team["id"] for team in updated_teams)

    assert id not in ids

async def test_delete_team_no_auth(auth_client_teams):
    teams = (await auth_client_teams.get(
        "/leagues/1/teams"
    )).json()["teams"]

    team_to_delete = teams[0]

    id = team_to_delete["id"]

    response = await auth_client_teams.noauth_delete(
        f"/leagues/1/teams/{id}"
    )

    assert response.status_code == 401

    updated_teams = (await auth_client_teams.get(
        "/leagues/1/teams"
    )).json()["teams"]

    assert len(updated_teams) == len(teams)

async def test_delete_team_wrong_id(auth_client_teams):
    teams = (await auth_client_teams.get(
        "/leagues/1/teams"
    )).json()["teams"]

    response = await auth_client_teams.delete(
        "/leagues/1/teams/9999"
    )

    assert response.status_code == 404

    updated_teams = (await auth_client_teams.get(
        "/leagues/1/teams"
    )).json()["teams"]

    assert len(updated_teams) == len(teams)