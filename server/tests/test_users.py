# Registration endpoint testing

def test_registration(client, helpers):
    response = helpers.register_user(client)

    assert response["email"] == "authuser@example.com"
    assert response["username"] == "authusername"


def test_duplicate_email_registration(client, helpers):
    user = helpers.register_user(client)

    user["username"] = "newusername"
    response = client.post("/users/", json=user)

    assert response.status_code == 409

def test_duplicate_username_registration(client, helpers):
    user = helpers.register_user(client)

    user["email"] = "newusername@example.com"
    response = client.post("/users/", json=user)

    assert response.status_code == 409

def test_duplicate_password_ok(client, helpers):
    user = helpers.register_user(client)

    user["email"] = "newusername@example.com"
    user["username"] = "newusername"

    response = client.post("/users/", json=user)

    assert response.status_code == 201

def test_missing_username_registration(client):
    user = {
        "email": "missingdata@example.com",
        "password": "missingdata"
    }

    response = client.post("/users/", json=user)

    assert response.status_code == 422

def test_missing_email_registration(client):
    user = {
        "username": "missingdatauser",
        "password": "missingdata"
    }

    response = client.post("/users/", json=user)

    assert response.status_code == 422

def test_missing_password_registration(client):
    user = {
        "email": "missingdata@example.com",
        "username": "missingdata"
    }

    response = client.post("/users/", json=user)

    assert response.status_code == 422

def test_incorrect_email_type(client):
    user = {
        "email": "incorrectgmail.com",
        "username": "incorrect",
        "password": "password"
    }

    response = client.post("/users/", json=user)

    assert response.status_code == 422


# Login endpoint testing

def test_login_email(client, helpers):
    response = helpers.full_login(client)

    assert "access_token" in response

def test_login_username(client, helpers):
    user = helpers.register_user(client)

    response = client.post(
        "/users/login",
        data={
            "username": user["username"],
            "password": user["password"]
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_incorrect_password(client, helpers):
    user = helpers.register_user(client)

    response = client.post(
        "/users/login",
        data={
            "username": user["email"],
            "password": "incorrectpassword"
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    assert response.status_code == 403

def test_incorrect_email(client, helpers):
    user = helpers.register_user(client)

    response = client.post(
        "/users/login",
        data={
            "username": "notroot",
            "password": user["password"]
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        }
    )

    assert response.status_code == 403


# test update endpoint

def test_update_email(client, helpers):
    user = helpers.full_login(client)

    updated_payload = {
        "updated_user": {
            "email": "newemail@example.com",
            "username": user["username"],
            "password": user["password"]
        },
        "password": user["password"]
    }
    response = helpers.update_user(client, updated_payload, user)

    assert response["email"] == "newemail@example.com"
    assert response["username"] == user["username"]

def test_update_username(client, helpers):
    user = helpers.full_login(client)
    updated_payload = {
        "updated_user": {
            "email": user["email"],
            "username": "newusername",
            "password": user["password"]
        },
        "password": user["password"]
    }
    response = helpers.update_user(client, updated_payload, user)

    assert response["email"] == user["email"]
    assert response["username"] == "newusername"

def test_update_password(client, helpers):
    user = helpers.full_login(client)

    updated_payload = {
        "updated_user": {
            "email": user["email"],
            "username": user["username"],
            "password": "newpassword"
        },
        "password": user["password"]
    }

    response = helpers.update_user(client, updated_payload, user)

    assert response["email"] == user["email"]
    assert response["username"] == user["username"]

def test_update_incorrect_password(client, helpers):
    user = helpers.full_login(client)

    updated_payload = {
        "updated_user": {
            "email": "newemail@example.com",
            "username": user["username"],
            "password": user["password"]
        },
        "password": "incorrect"
    }
    response = client.put(
        "/users/",
        json=updated_payload,
        headers=helpers.auth_headers(user)
        )
    
    assert response.status_code == 401

def test_update_same_info(client, helpers):
    user = helpers.full_login(client)

    updated_payload = {
        "updated_user": {
            "email": user["email"],
            "username": user["username"],
            "password": user["password"]
        },
        "password": user["password"]
    }
    response = client.put(
        "/users/",
        json=updated_payload,
        headers=helpers.auth_headers(user)
        )
    
    assert response.status_code == 400


# test delete endpoint


def test_delete(client, helpers):
    user = helpers.full_login(client)

    response = client.delete("/users/",
                             headers=helpers.auth_headers(user)
                             )
    
    assert response.status_code == 204

def test_delete_not_logged_in(client, helpers):
    user = helpers.register_user(client)

    response = client.delete("/users/")

    assert response.status_code == 401

def test_delete_logged_in_no_headers(client, helpers):
    response = helpers.full_login(client)

    response = client.delete("/users/")

    assert response.status_code == 401