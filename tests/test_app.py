from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_duplicate_signup_is_rejected():
    activity_name = "Chess Club"
    email = "student@example.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert response.status_code == 200

    duplicate_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert duplicate_response.status_code == 400
    assert "already signed up" in duplicate_response.json()["detail"].lower()


def test_unregister_participant_removes_email():
    activity_name = "Science Club"
    email = "remove-me@example.edu"

    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert signup_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/participants?email={email}")
    assert delete_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]
