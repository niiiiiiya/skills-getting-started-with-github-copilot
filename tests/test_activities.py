import uuid

from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def unique_email():
    return f"test-{uuid.uuid4().hex}@mergington.edu"


def activity_participants(activity_id: str):
    resp = client.get("/activities")
    resp.raise_for_status()
    data = resp.json()
    return data[activity_id]["participants"]


def signup(activity_id: str, email: str):
    return client.post(f"/activities/{activity_id}/signup", params={"email": email})


def unregister(activity_id: str, email: str):
    return client.delete(f"/activities/{activity_id}/signup", params={"email": email})


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "chess-club" in data


def test_signup_and_unregister_cycle():
    activity_id = "chess-club"
    email = unique_email()

    # Ensure not present
    participants_before = activity_participants(activity_id)
    assert email not in participants_before

    # Sign up
    resp = signup(activity_id, email)
    assert resp.status_code == 200
    assert f"Signed up {email}" in resp.json().get("message", "")

    # Verify added
    participants_after = activity_participants(activity_id)
    assert email in participants_after

    # Duplicate signup -> 400
    resp_dup = signup(activity_id, email)
    assert resp_dup.status_code == 400

    # Unregister
    resp_del = unregister(activity_id, email)
    assert resp_del.status_code == 200
    assert f"Removed {email}" in resp_del.json().get("message", "")

    # Verify removed
    participants_final = activity_participants(activity_id)
    assert email not in participants_final
