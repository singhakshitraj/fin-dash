import pytest
from fastapi import status

def test_user_registration(client):
    response = client.post(
        "/auth/register",
        data={"username": "newuser", "password": "newpassword"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["username"] == "newuser"
    assert "access_token" in response.json()

def test_user_login(client):
    # First, register a user
    client.post(
        "/auth/register",
        data={"username": "loginuser", "password": "loginpassword"}
    )
    # Then login
    response = client.post(
        "/auth/login",
        data={"username": "loginuser", "password": "loginpassword"}
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "loginuser"
    assert "access_token" in response.json()

def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login",
        data={"username": "nonexistent", "password": "wrongpassword"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "message" in response.json()["detail"]
