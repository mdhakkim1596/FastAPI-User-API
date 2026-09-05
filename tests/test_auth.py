from tests.conftest import client, get_token


def test_login_success():
    get_token()
    response = client.post(
        "/auth/login", json={"email": "authuser@gmail.com", "password": "Testuser@123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_user_not_found():
    response = client.post(
        "/auth/login", json={"email": "notexist@gmail.com", "password": "Testuser@123"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_login_wrong_password():
    get_token()
    response = client.post(
        "/auth/login", json={"email": "authuser@gmail.com", "password": "WrongPass@123"}
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Wrong password"
