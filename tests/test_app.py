from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities_returns_all_activities():
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_adds_participant_to_activity():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Ensure the participant is not already present before the request
    assert email not in client.get("/activities").json()[activity_name]["participants"]

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity_name}"}
    assert email in client.get("/activities").json()[activity_name]["participants"]


def test_duplicate_signup_returns_400():
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"


def test_delete_participant_from_activity():
    activity_name = "Gym Class"
    email = "john@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    assert response.status_code == 200
    assert response.json() == {"message": f"Removed {email} from {activity_name}"}
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_delete_non_existent_participant_returns_404():
    activity_name = "Gym Class"
    email = "missingstudent@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
