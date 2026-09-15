from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    # Arrange
    activity_name = "Chess Club"
    email = "student@example.edu"

    # Act
    first_signup = client.post(f"/activities/{activity_name}/signup?email={email}")
    duplicate_signup = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert first_signup.status_code == 200
    assert duplicate_signup.status_code == 400
    assert "already signed up" in duplicate_signup.json()["detail"].lower()


def test_unregister_participant_removes_email():
    # Arrange
    activity_name = "Science Club"
    email = "remove-me@example.edu"

    # Act
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    activities_response = client.get("/activities")

    # Assert
    assert signup_response.status_code == 200
    assert delete_response.status_code == 200
    assert email not in activities_response.json()[activity_name]["participants"]
