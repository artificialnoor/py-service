def test_register_login_me(client, auth_headers):
    resp = client.get("/api/v1/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["email"] == "admin@example.com"


def test_duplicate_register(client, auth_headers):
    resp = client.post(
        "/api/v1/auth/register", json={"email": "admin@example.com", "password": "another-pass"}
    )
    assert resp.status_code == 409


def test_bad_login(client, auth_headers):
    resp = client.post(
        "/api/v1/auth/login", data={"username": "admin@example.com", "password": "wrong"}
    )
    assert resp.status_code == 401


def test_me_requires_token(client):
    assert client.get("/api/v1/auth/me").status_code == 401
    bad = {"Authorization": "Bearer not-a-jwt"}
    assert client.get("/api/v1/auth/me", headers=bad).status_code == 401
