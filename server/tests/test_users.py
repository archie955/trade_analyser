# Registration endpoint testing

def test_registration(client):
    response = client.post(
        "/users/",
        json={
            "email": "test@example.com",
            "username": "testusername",
            "password": "testpassword"
        }
    )

    assert response.status_code == 201

    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testusername"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_duplicate_email_registration(client):
    user = {
        "email": "duplicate@example.com",
        "username": "duplicateusername",
        "password": "duplicatepassword"
    } 

    client.post("/users/", json=user)

    user["username"] = "newusername"
    response = client.post("/users/", json=user)

    assert response.status_code == 409

def test_duplicate_username_registration(client):
    user = {
        "email": "duplicate@example.com",
        "username": "duplicateusername",
        "password": "duplicatepassword"
    } 

    client.post("/users/", json=user)

    user["email"] = "newusername@example.com"
    response = client.post("/users/", json=user)

    assert response.status_code == 409

def test_duplicate_password_ok(client):
    user = {
        "email": "duplicate@example.com",
        "username": "duplicateusername",
        "password": "duplicatepassword"
    }

    client.post("/users/", json=user)

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

def test_login_email(client):
    user = {
        "email": "root@email.com",
        "username": "root",
        "password": "passwordroot"
    }
    client.post("/users/", json=user)

    response = client.post(
        "/users/login",
        data={
            "username": user["email"],
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

def test_login_username(client):
    user = {
        "email": "root@email.com",
        "username": "root",
        "password": "passwordroot"
    }
    client.post("/users/", json=user)

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

def test_incorrect_password(client):
    user = {
        "email": "root@email.com",
        "username": "root",
        "password": "passwordroot"
    }
    client.post("/users/", json=user)

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

def test_incorrect_email(client):
    user = {
        "email": "root@email.com",
        "username": "root",
        "password": "passwordroot"
    }
    client.post("/users/", json=user)

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

def test_update_email(client, authenticated_user, helpers):
    user = helpers.register_user(client)
    updated_payload = {
        "updated_user": {
            "email": "newemail@example.com",
            "username": user["username"],
            "password": user["password"]
        },
        "password": user["password"]
    }
    response = client.put(
        "/users/",
        json=updated_payload,
        headers=helpers.auth_headers(authenticated_user)
        )
    
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == "newemail@example.com"
    assert data["username"] == user["username"]

def test_update_username(client, authenticated_user, helpers):
    user = {
        "email": "authuser@example.com",
        "username": "authusername",
        "password": "authpassword"
    }
    updated_payload = {
        "updated_user": {
            "email": user["email"],
            "username": "newusername",
            "password": user["password"]
        },
        "password": user["password"]
    }
    response = client.put(
        "/users/",
        json=updated_payload,
        headers=helpers.auth_headers(authenticated_user)
        )
    
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == user["email"]
    assert data["username"] == "newusername"

def test_update_password(client, authenticated_user, helpers):
    user = {
        "email": "authuser@example.com",
        "username": "authusername",
        "password": "authpassword"
    }
    updated_payload = {
        "updated_user": {
            "email": user["email"],
            "username": user["username"],
            "password": "newpassword"
        },
        "password": user["password"]
    }
    response = client.put(
        "/users/",
        json=updated_payload,
        headers=helpers.auth_headers(authenticated_user)
        )
    
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == user["email"]
    assert data["username"] == user["username"]

def test_update_incorrect_password(client, authenticated_user, helpers):
    user = {
        "email": "authuser@example.com",
        "username": "authusername",
        "password": "authpassword"
    }
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
        headers=helpers.auth_headers(authenticated_user)
        )
    
    assert response.status_code == 401

def test_update_same_info(client, authenticated_user, helpers):
    user = {
        "email": "authuser@example.com",
        "username": "authusername",
        "password": "authpassword"
    }
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
        headers=helpers.auth_headers(authenticated_user)
        )
    
    assert response.status_code == 400


# test delete endpoint


def test_delete(client, authenticated_user, helpers):
    response = client.delete("/users/",
                             headers=helpers.auth_headers(authenticated_user)
                             )
    assert response.status_code == 204

def test_delete_no_auth(client, authenticated_user):
    response = client.delete("/users/",
                             headers=None
                             )
    assert response.status_code == 401