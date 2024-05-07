# test_user_routes.py
from builtins import RuntimeError, ValueError, isinstance, str
import pytest
from app.utils.security import hash_password, verify_password

def test_create_user(client):
    response = client.post("/users/", json={
        "email": "newuser@example.com",
        "password": "strongpassword"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "newuser@example.com"

def test_create_user_existing_email(client):
    response = client.post("/users/", json={
        "email": "existing@example.com",
        "password": "password"
    })
    assert response.status_code == 400

def test_get_user(client):
    response = client.get("/users/{user_id}")  # Assume a valid UUID
    assert response.status_code == 200
    assert 'email' in response.json()

def test_get_nonexistent_user(client):
    response = client.get("/users/{nonexistent_user_id}")
    assert response.status_code == 404

def test_update_user(client):
    response = client.put("/users/{user_id}", json={
        "nickname": "UpdatedNickname"
    })
    assert response.status_code == 200
    assert response.json()["nickname"] == "UpdatedNickname"

def test_delete_user(client):
    response = client.delete("/users/{user_id}")
    assert response.status_code == 204

def test_list_users(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert type(response.json()["items"]) is list

def test_register_user(client):
    response = client.post("/register/", json={
        "email": "register@example.com",
        "password": "password"
    })
    assert response.status_code == 201

def test_login_user(client):
    response = client.post("/login/", data={
        "username": "user@example.com",
        "password": "password"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_verify_email(client):
    response = client.get("/verify-email/{user_id}/{token}")
    assert response.status_code == 200
    assert response.json()["message"] == "Email verified successfully"
