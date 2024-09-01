import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/register/", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 201
    assert response.json() == {"message": "User registered successfully"}

def test_get_token():
    response = client.post(
        "/token/",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_create_note():
    # Получение токена
    response = client.post(
        "/token/",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    token = response.json()["access_token"]

    # Создание заметки
    response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "This is a test note."},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Note"
    assert response.json()["content"] == "This is a test note."
