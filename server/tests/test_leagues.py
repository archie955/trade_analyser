def test_create_league(auth_client):
    response = auth_client.post("/leagues/", json={"name": "testleague"})

    print(response)
    assert response.status_code == 201
    data = response.json()

    assert data["name"] == "testleague"
    assert "created_at" in data
    assert "id" in data
    assert "updated_at" in data