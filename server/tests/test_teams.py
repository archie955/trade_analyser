def test_create_team(auth_client_leagues):
    response = auth_client_leagues.post(
        "/teams/1",
        json={"name": "team_1"}
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == "team_1"
    assert data["league_id"] == 1
    assert "created_at" in data
    assert "id" in data
    assert "updated_at" in data

def test_no_auth_create_team(auth_client_leagues):
    response = auth_client_leagues.noauth_post(
        "/teams/1",
        json={"name": "testteamnoauth"}
    )

    assert response.status_code == 401

def test_create_team_wrong_payload(auth_client_leagues):
    response = auth_client_leagues.post(
        "/teams/1",
        json={"wrong": "testteam"}
    )

    assert response.status_code == 422

def test_create_team_same_name(auth_client_teams):
    response = auth_client_teams.post(
        "/teams/1",
        json={"name": "team_1"}
    )

    assert response.status_code == 400

def test_get_teams(auth_client_teams):
    response = auth_client_teams.get(
        "/teams/1"
    )

    assert response.status_code == 200

    data = response.json()["teams"]

    assert len(data) == 2
    
    team = data[0]
    assert team["name"] == "team_1"
    assert team["league_id"] == 1
    assert "created_at" in team
    assert "id" in team
    assert "updated_at" in team 

def test_get_teams_no_auth(auth_client_teams):
    response = auth_client_teams.noauth_get(
        "/teams/1"
    )

    assert response.status_code == 401

def test_get_no_teams(auth_client_leagues):
    response = auth_client_leagues.get(
        "/teams/1"
    )

    assert response.status_code == 200
    data = response.json()["teams"]

    assert len(data) == 0

def test_update_team(auth_client_teams):
    team_to_update = auth_client_teams.get(
        "/teams/1"
    ).json()["teams"][0]

    updated = {"id": team_to_update["id"], "name": "newname"}

    response = auth_client_teams.put(
        "/teams/1",
        json=updated
    )

    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "newname"
    assert data["league_id"] == 1
    assert "created_at" in data
    assert "id" in data
    assert "updated_at" in data

def test_update_team_missing_name(auth_client_teams):
    team_to_update = auth_client_teams.get(
        "/teams/1"
    ).json()["teams"][0]

    updated = {"id": team_to_update["id"]}

    response = auth_client_teams.put(
        "/teams/1",
        json=updated
    )

    assert response.status_code == 422

def test_update_team_wrong_id(auth_client_teams):
    updated = {"id": 9999, "name": "newname"}

    response = auth_client_teams.put(
        "/teams/1",
        json=updated
    )

    assert response.status_code == 404

def test_update_team_not_auth(auth_client_teams):
    team_to_update = auth_client_teams.get(
        "/teams/1"
    ).json()["teams"][0]

    updated = {"id": team_to_update["id"], "name": "newname"}

    response = auth_client_teams.noauth_put(
        "/teams/1",
        json=updated
    )

    assert response.status_code == 401

def test_delete_team(auth_client_teams):
    teams = auth_client_teams.get(
        "/teams/1"
    ).json()["teams"]

    team_to_delete = teams[0]

    id = team_to_delete["id"]

    response = auth_client_teams.delete(
        f"/teams/1/{id}"
    )

    assert response.status_code == 204

    updated_teams = auth_client_teams.get(
        "/teams/1"
    ).json()["teams"]

    assert len(updated_teams) == len(teams) - 1

    ids = set(team["id"] for team in updated_teams)

    assert id not in ids

def test_delete_team_no_auth(auth_client_teams):
    teams = auth_client_teams.get(
        "/teams/1"
    ).json()["teams"]

    team_to_delete = teams[0]

    id = team_to_delete["id"]

    response = auth_client_teams.noauth_delete(
        f"/teams/1/{id}"
    )

    assert response.status_code == 401

    updated_teams = auth_client_teams.get(
        "/teams/1"
    ).json()["teams"]

    assert len(updated_teams) == len(teams)

def test_delete_team_wrong_id(auth_client_teams):
    teams = auth_client_teams.get(
        "/teams/1"
    ).json()["teams"]

    response = auth_client_teams.delete(
        "/teams/1/9999"
    )

    assert response.status_code == 404

    updated_teams = auth_client_teams.get(
        "/teams/1"
    ).json()["teams"]

    assert len(updated_teams) == len(teams)