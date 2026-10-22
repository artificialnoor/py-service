SERVICE = {
    "name": "Oil Change",
    "slug": "oil-change",
    "description": "Full synthetic oil change",
    "price": "49.99",
    "duration_minutes": 30,
}


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_requires_auth(client):
    assert client.post("/api/v1/services", json=SERVICE).status_code == 401


def test_crud(client, auth_headers):
    created = client.post("/api/v1/services", json=SERVICE, headers=auth_headers)
    assert created.status_code == 201
    sid = created.json()["id"]

    listed = client.get("/api/v1/services").json()
    assert [s["slug"] for s in listed] == ["oil-change"]

    patched = client.patch(f"/api/v1/services/{sid}", json={"price": "59.00"}, headers=auth_headers)
    assert patched.json()["price"] == "59.00"

    assert client.delete(f"/api/v1/services/{sid}", headers=auth_headers).status_code == 204
    assert client.get(f"/api/v1/services/{sid}").status_code == 404


def test_validation(client, auth_headers):
    bad = {**SERVICE, "slug": "Not A Slug", "price": "-1"}
    resp = client.post("/api/v1/services", json=bad, headers=auth_headers)
    assert resp.status_code == 422


def test_duplicate_slug(client, auth_headers):
    client.post("/api/v1/services", json=SERVICE, headers=auth_headers)
    resp = client.post("/api/v1/services", json=SERVICE, headers=auth_headers)
    assert resp.status_code == 409


def test_inactive_hidden_by_default(client, auth_headers):
    client.post("/api/v1/services", json={**SERVICE, "is_active": False}, headers=auth_headers)
    assert client.get("/api/v1/services").json() == []
    assert len(client.get("/api/v1/services?include_inactive=true").json()) == 1
