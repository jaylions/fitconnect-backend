from __future__ import annotations

from typing import Iterator

import numpy as np
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.settings import settings
from app.db.base import Base
from app.models.embeddings import TalentEmbedding
from app.models.profile import TalentProfile
from app.models.user import User
from app.services import embedding_sync_service
from app.services.embedding_sync_service import DEFAULT_MODEL


@pytest.fixture
def db_session() -> Iterator[Session]:
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
    with SessionLocal() as session:
        yield session


def _add_talent_user(session: Session, user_id: int) -> None:
    with session.begin():
        session.add(
            User(id=user_id, email=f"talent{user_id}@example.com", password_hash="x", role="talent")
        )
        session.add(TalentProfile(user_id=user_id))


def test_upsert_embeddings_applied(db_session: Session) -> None:
    _add_talent_user(db_session, user_id=1)
    vector = (np.ones(4, dtype=np.float32) / 2.0).tolist()

    result = embedding_sync_service.upsert_embeddings_for_user(
        db_session,
        user_id=1,
        role="talent",
        facets={"vector_roles": {"embedding": vector}},
        dim=4,
    )

    assert result.status == "applied"
    row = db_session.get(TalentEmbedding, 1)
    assert row is not None
    stored = np.asarray(row.vector_roles["embedding"], dtype=np.float32)
    assert pytest.approx(float(np.linalg.norm(stored)), rel=1e-6, abs=1e-6) == 1.0


def test_upsert_embeddings_records_warning(db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    _add_talent_user(db_session, user_id=2)
    vector = [2.0, 0.0, 0.0, 0.0]

    result = embedding_sync_service.upsert_embeddings_for_user(
        db_session,
        user_id=2,
        role="talent",
        facets={"vector_roles": {"embedding": vector}},
        dim=4,
    )

    assert result.status == "partial"
    assert "vector_roles:normalised" in result.warnings


def test_upsert_embeddings_pipeline_failure(db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    _add_talent_user(db_session, user_id=3)

    monkeypatch.setattr(
        embedding_sync_service,
        "embed_text",
        lambda text, *, model=DEFAULT_MODEL, dim=1536: None,
    )

    result = embedding_sync_service.upsert_embeddings_for_user(
        db_session,
        user_id=3,
        role="talent",
        facets={"vector_roles": {"text": "hello world"}},
        dim=4,
    )

    assert result.status == "error"
    assert result.errors["vector_roles"] == "embedding_pipeline_unavailable"


def test_upsert_embeddings_respects_feature_flag(db_session: Session, monkeypatch: pytest.MonkeyPatch) -> None:
    _add_talent_user(db_session, user_id=4)
    monkeypatch.setattr(settings, "MATCHING_SYNC_ENABLED", False)

    result = embedding_sync_service.upsert_embeddings_for_user(
        db_session,
        user_id=4,
        role="talent",
        facets={"vector_roles": {"embedding": [1.0, 0.0, 0.0, 0.0]}},
        dim=4,
    )

    assert result.status == "disabled"
    row = db_session.get(TalentEmbedding, 4)
    assert row is None


def test_delete_embeddings_clears_facets(db_session: Session) -> None:
    _add_talent_user(db_session, user_id=5)
    vector = (np.ones(4, dtype=np.float32) / 2.0).tolist()
    embedding_sync_service.upsert_embeddings_for_user(
        db_session,
        user_id=5,
        role="talent",
        facets={"vector_roles": {"embedding": vector}},
        dim=4,
    )

    result = embedding_sync_service.delete_embeddings_for_user(db_session, user_id=5, role="talent")
    assert result.status == "applied"
    row = db_session.get(TalentEmbedding, 5)
    assert row is not None
    assert row.vector_roles is None
