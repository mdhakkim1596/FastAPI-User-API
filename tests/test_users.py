from tests.conftest import client, get_token


def test_create_user():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testaccount@gmail.com",
            "age": 25,
            "phone_number": "+919876543021",
            "gender": "Male",
            "password": "Testuser@123",
            "confirm_password": "Testuser@123",
        },
    )
    assert response.status_code == 200
    assert response.json()["email"] == "testaccount@gmail.com"
    assert "password" not in response.json()


def test_create_user_invalid_email():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testaccount@yahoo.com",
            "age": 25,
            "phone_number": "+919876543021",
            "gender": "Male",
            "password": "Testuser@123",
            "confirm_password": "Testuser@123",
        },
    )
    assert response.status_code == 422


def test_create_user_weak_password():
    response = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testaccount1@gmail.com",
            "age": 25,
            "phone_number": "+919876543021",
            "gender": "Male",
            "password": "password",
            "confirm_password": "password",
        },
    )
    assert response.status_code == 422


def test_create_user_password_mismatch():
    responce = client.post(
        "/users",
        json={
            "name": "Test User",
            "email": "testaccount2@gmail.com",
            "age": 25,
            "phone_number": "+919876543021",
            "gender": "Male",
            "password": "Testuser@123",
            "confirm_password": "Testuser@124",
        },
    )
    assert responce.status_code == 422


def test_get_user():
    token = get_token()
    responce = client.get("/users/1", headers={"Authorization": f"Bearer {token}"})
    assert responce.status_code == 200
    assert responce.json()["email"] == "authuser@gmail.com"


def test_get_user_not_found():
    token = get_token()
    responce = client.get("/users/999", headers={"Authorization": f"Bearer {token}"})
    assert responce.status_code == 404
    assert responce.json()["detail"] == "User not found"


def test_get_user_without_token():
    response = client.get("/users/1")
    assert response.status_code == 401


def test_delete_user():
    token = get_token()
    response = client.delete("/users/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "User deleted successfully"


def test_delete_user_not_found():
    token = get_token()
    response = client.delete("/users/999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_patch_user():
    token = get_token()
    response = client.patch(
        "/users/1",
        json={"name": "Updated Name"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["email"] == "authuser@gmail.com"


def test_get_all_users():
    token = get_token()
    response = client.get("/users", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1
    assert response.json()[0]["email"] == "authuser@gmail.com"


def test_put_user():
    token = get_token()
    response = client.put(
        "/users/1",
        json={
            "name": "Updated User",
            "email": "authuser@gmail.com",
            "age": 26,
            "phone_number": "+919876543021",
            "gender": "Male",
            "password": "Testuser@123",
            "confirm_password": "Testuser@123",
            "home_address": "None",
            "office_address": "None",
            "occupation": "None"
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated User"
    assert response.json()["age"] == 26
