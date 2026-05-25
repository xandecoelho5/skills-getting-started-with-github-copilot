import urllib.parse

from src import app as app_module
from src.app import activities


def test_get_activities_returns_all(client):
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Expect known activity keys
    assert "Chess Club" in data


def test_signup_success_and_appears(client):
    email = "tester@mergington.edu"
    activity = "Chess Club"
    path = f"/activities/{urllib.parse.quote(activity, safe='')}" + f"/signup?email={urllib.parse.quote(email, safe='')}"
    res = client.post(path)
    assert res.status_code == 200
    assert "Signed up" in res.json().get("message", "")

    get = client.get("/activities")
    assert email in get.json()[activity]["participants"]


def test_signup_duplicate_and_capacity(client):
    # create a tiny activity with capacity 1
    activities["Tiny"] = {
        "description": "Tiny activity",
        "schedule": "Now",
        "max_participants": 1,
        "participants": [],
    }

    email = "a@mergington.edu"
    path = f"/activities/{urllib.parse.quote('Tiny', safe='')}" + f"/signup?email={urllib.parse.quote(email, safe='')}"
    res1 = client.post(path)
    assert res1.status_code == 200

    # duplicate
    res2 = client.post(path)
    assert res2.status_code == 400

    # another participant should hit capacity
    path_b = f"/activities/{urllib.parse.quote('Tiny', safe='')}" + f"/signup?email={urllib.parse.quote('b@mergington.edu', safe='')}"
    res3 = client.post(path_b)
    assert res3.status_code == 400


def test_remove_participant_success_and_not_found(client):
    activity = "Chess Club"
    existing = activities[activity]["participants"][0]

    del_path = f"/activities/{urllib.parse.quote(activity, safe='')}" + f"/participants?email={urllib.parse.quote(existing, safe='')}"
    res = client.delete(del_path)
    assert res.status_code == 200

    # deleting again yields 404
    res2 = client.delete(del_path)
    assert res2.status_code == 404
