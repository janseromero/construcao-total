"""Pytest fixtures: app + SQLite em memória."""

import os
from collections.abc import Iterator

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["JWT_SECRET"] = "test-secret"

import contextlib

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from app.db import session as session_module  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def _setup_db():
    test_engine = create_engine("sqlite:///./test.db", future=True)
    session_module.engine = test_engine
    session_module.SessionLocal = sessionmaker(
        bind=test_engine, autoflush=False, autocommit=False, future=True
    )

    import app.models  # noqa: F401
    from app.db.base import Base

    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)
    with contextlib.suppress(OSError):
        os.remove("./test.db")


@pytest.fixture
def client() -> Iterator[TestClient]:
    from app.main import app

    with TestClient(app) as c:
        yield c


@pytest.fixture
def db():
    from app.db.session import SessionLocal

    s = SessionLocal()
    try:
        yield s
    finally:
        s.close()


def signup(client: TestClient, *, cnpj: str, email: str) -> str:
    r = client.post(
        "/auth/signup",
        json={
            "construtora_nome": f"Construtora {cnpj}",
            "cnpj": cnpj,
            "user_nome": "Owner",
            "email": email,
            "password": "supersecret",
        },
    )
    assert r.status_code == 201, r.text
    return r.json()["access_token"]


def auth_headers(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}
