import json

def test_get_campers(client):
    res = client.get("/campers")
    assert res.status_code == 200
    assert isinstance(res.json, list)

def test_create_camper_success(client, db):
    res = client.post("/campers", json={"name": "Zoe", "age": 11})
    assert res.status_code == 201
    assert res.json["name"] == "Zoe"
    assert res.json["age"] == 11

def test_create_camper_validation(client):
    res = client.post("/campers", json={"name": "", "age": 5})
    assert res.status_code == 400
    assert "errors" in res.json

def test_get_single_camper_not_found(client):
    res = client.get("/campers/999")
    assert res.status_code == 404
    assert res.json["error"] == "Camper not found"

def test_patch_camper_success(client, db):
    res = client.post("/campers", json={"name": "Amy", "age": 12})
    camper_id = res.json["id"]

    res2 = client.patch(f"/campers/{camper_id}", json={"name": "Updated"})
    assert res2.status_code == 202
    assert res2.json["name"] == "Updated"

def test_get_activities(client):
    res = client.get("/activities")
    assert res.status_code == 200
    assert isinstance(res.json, list)

def test_delete_activity_not_found(client):
    res = client.delete("/activities/999")
    assert res.status_code == 404
    assert res.json["error"] == "Activity not found"

def test_create_signup_success(client, db):
    camper = client.post("/campers", json={"name": "Tom", "age": 10}).json
    activity = client.post("/activities", json={"name": "Archery", "difficulty": 2}).json

    res = client.post("/signups", json={
        "camper_id": camper["id"],
        "activity_id": activity["id"],
        "time": 10
    })

    assert res.status_code == 201
    assert "activity" in res.json
    assert "camper" in res.json

def test_create_signup_validation(client):
    res = client.post("/signups", json={"camper_id": 1, "activity_id": 1, "time": 30})
    assert res.status_code == 400
    assert "errors" in res.json
