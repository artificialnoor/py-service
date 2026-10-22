from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import get_db
from app.main import app
from app.models import Base


@pytest.fixture
def db() -> Generator[Session]:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with TestingSession() as session:
        yield session
    engine.dispose()


@pytest.fixture
def client(db: Session) -> Generator[TestClient]:
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client: TestClient) -> dict[str, str]:
    creds = {"email": "admin@example.com", "password": "s3cret-pass"}
    client.post("/api/v1/auth/register", json=creds)
    resp = client.post(
        "/api/v1/auth/login", data={"username": creds["email"], "password": creds["password"]}
    )
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}
