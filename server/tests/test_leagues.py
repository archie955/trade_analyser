def test_create_league(auth_client):
    response = auth_client.post(
        "/leagues/",
        json={"name": "testleague"}
    )

    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "testleague"
    assert "created_at" in data
    assert "id" in data
    assert "updated_at" in data

def test_no_auth_create_league(auth_client):
    response = auth_client.noauth_post(
        "/leagues/",
        json={"name": "testleaguenoauth"}
    )

    assert response.status_code == 401

def test_create_league_wrong_payload(auth_client_leagues):
    response = auth_client_leagues.post(
        "/leagues/",
        json={"wrong": "testleague"}
    )

    assert response.status_code == 422

def test_create_league_same_name(auth_client):
    auth_client.post(
        "/leagues/",
        json={"name": "testleague"}
    )

    response = auth_client.post(
        "/leagues/",
        json={"name": "testleague"}
    )

    response.status_code == 400

def test_get_leagues(auth_client_leagues):
    response = auth_client_leagues.get(
        "/leagues/"
    )

    assert response.status_code == 200
    data = response.json()["leagues"]

    assert len(data) == 2
    assert "created_at" in data[0]
    assert "id" in data[0]
    assert "updated_at" in data[0]

    names = set(data[i]["name"] for i in range(2))

    assert "league_1" in names
    assert "league_2" in names

def test_get_leagues_no_auth(auth_client_leagues):
    response = auth_client_leagues.noauth_get(
        "/leagues/"
    )

    assert response.status_code == 401

def test_get_no_leagues(auth_client):
    response = auth_client.get(
        "/leagues/"
    )

    assert response.status_code == 200
    data = response.json()["leagues"]

    assert len(data) == 0

def test_update_league(auth_client_leagues):
    leagues = auth_client_leagues.get(
        "/leagues/"
    ).json()["leagues"]

    league_to_update = leagues[0]

    updated = {"id": league_to_update["id"], "name": "newname"}

    response = auth_client_leagues.put(
        "/leagues/",
        json=updated
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "newname"
    assert "created_at" in data
    assert "id" in data
    assert "updated_at" in data

def test_update_league_missing_name(auth_client_leagues):
    leagues = auth_client_leagues.get(
        "/leagues/"
    ).json()["leagues"]

    league_to_update = leagues[0]

    updated = {"id": league_to_update["id"]}

    response = auth_client_leagues.put(
        "/leagues/",
        json=updated
    )

    assert response.status_code == 422

def test_update_league_wrong_id(auth_client_leagues):
    updated = {"id": 999999, "name": "newname"}

    response = auth_client_leagues.put(
        "/leagues/",
        json=updated
    )

    assert response.status_code == 404

def test_update_league_no_auth(auth_client_leagues):
    leagues = auth_client_leagues.get(
        "/leagues/"
    ).json()["leagues"]

    league_to_update = leagues[0]

    updated = {"id": league_to_update["id"], "name": "newname"}

    response = auth_client_leagues.noauth_put(
        "/leagues/",
        json=updated
    )

    assert response.status_code == 401

def test_delete_league(auth_client_leagues):
    leagues = auth_client_leagues.get(
        "/leagues/"
    ).json()["leagues"]

    league_to_delete = leagues[0]

    id = league_to_delete["id"]

    response = auth_client_leagues.delete(
        f"/leagues/{id}"
    )

    assert response.status_code == 204

    updated_leagues = auth_client_leagues.get(
        "/leagues/"
    ).json()["leagues"]

    assert len(updated_leagues) == len(leagues) - 1

    ids = set(league["id"] for league in updated_leagues)

    assert id not in ids

def test_delete_league_no_auth(auth_client_leagues):
    leagues = auth_client_leagues.get(
        "/leagues/"
    ).json()["leagues"]

    league_to_delete = leagues[0]

    id = league_to_delete["id"]

    response = auth_client_leagues.noauth_delete(
        f"/leagues/{id}"
    )

    assert response.status_code == 401

    updated_leagues = auth_client_leagues.get(
        "/leagues/"
    ).json()["leagues"]

    assert len(leagues) == len(updated_leagues)

def test_delete_league_wrong_id(auth_client_leagues):
    leagues = auth_client_leagues.get(
        "/leagues/"
    ).json()["leagues"]

    response = auth_client_leagues.delete(
        f"/leagues/{9999}"
    )

    response.status_code == 404

    updated_leagues = auth_client_leagues.get(
        "/leagues/"
    ).json()["leagues"]

    assert len(leagues) == len(updated_leagues)