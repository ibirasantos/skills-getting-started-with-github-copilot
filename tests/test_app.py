import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_for_activity():
    email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Remove if already present
    client.delete(f"/activities/{activity}/participant/{email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    data = response.json()
    assert f"Signed up {email} for {activity}" in data["message"]
    # Clean up
    client.delete(f"/activities/{activity}/participant/{email}")

def test_remove_participant():
    email = "removeuser@mergington.edu"
    activity = "Chess Club"
    # Ensure user is present
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/participant/{email}")
    assert response.status_code == 200
    data = response.json()
    assert f"Removed {email} from {activity}" in data["message"]
    # Try removing again, should 404
    response = client.delete(f"/activities/{activity}/participant/{email}")
    assert response.status_code == 404

def test_signup_duplicate():
    email = "duplicate@mergington.edu"
    activity = "Chess Club"
    # Ensure user is present
    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]
    # Clean up
    client.delete(f"/activities/{activity}/participant/{email}")
