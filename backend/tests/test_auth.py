import pytest


def test_login_success(client):
    response = client.post("/login", json={
        "username": "admin",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    response = client.post("/login", json={
        "username": "admin",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post("/login", json={
        "username": "xXx",
        "password": "aaa"
    })
    assert response.status_code == 401