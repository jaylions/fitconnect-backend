from __future__ import annotations

import math
from typing import Iterator, Tuple

import numpy as np
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.api.deps import get_current_user, get_db
from app.db.base import Base
from app.models.embeddings import TalentEmbedding
from app.models.profile import TalentProfile
from app.models.user import User
from app.services.embedding_validation import DEFAULT_EMBEDDING_DIM


@pytest.fixture
def api_client() -> Iterator[Tuple[TestClient, sessionmaker]]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(
        engine,
        tables=[
            User.__table__,
            TalentProfile.__table__,
            TalentEmbedding.__table__,
        ],
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

    def override_get_db() -> Iterator[Session]:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def override_get_current_user():
        return {"id": 1, "role": "talent"}

    from app.main import app  # Imported lazily to ensure settings are initialised

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    with SessionLocal.begin() as session:
        session.add(User(id=1, email="talent@example.com", password_hash="x", role="talent"))
        session.add(TalentProfile(user_id=1))

    client = TestClient(app)
    try:
        yield client, SessionLocal
    finally:
        app.dependency_overrides.clear()


def test_create_matching_vector_envelope(api_client):
    client, SessionLocal = api_client
    dim = DEFAULT_EMBEDDING_DIM
    component = 1.0 / math.sqrt(dim)
    vector = np.full(dim, component, dtype=np.float32).tolist()

    payload = {
        "role": "talent",
        "vector_roles": {"embedding": vector},
    }

    response = client.post("/api/me/matching-vectors", json=payload)
    assert response.status_code == 201
    body = response.json()
    assert body["ok"] is True
    assert "meta" not in body
    assert body["data"]["role"] == "talent"
    assert body["data"]["job_id"] is None

    with SessionLocal() as session:
        embedding = session.get(TalentEmbedding, 1)
        assert embedding is not None
        assert embedding.vector_roles is not None


def test_update_matching_vector(api_client):
    client, SessionLocal = api_client
    dim = 4
    base = 1.0 / math.sqrt(dim)
    create_payload = {
        "role": "talent",
        "vector_roles": {"embedding": [base] * dim},
    }
    response = client.post("/api/me/matching-vectors", json=create_payload)
    assert response.status_code == 201
    matching_id = response.json()["data"]["id"]

    update_payload = {
        "vector_skills": {"embedding": [base, 0.0, 0.0, 0.0]}
    }
    response = client.patch(f"/api/me/matching-vectors/{matching_id}", json=update_payload)
    assert response.status_code == 200
    body = response.json()
    assert body["data"]["id"] == matching_id
    assert "vector_skills" in body["data"]

    with SessionLocal() as session:
        embedding = session.get(TalentEmbedding, 1)
        assert embedding.vector_skills is not None
