from __future__ import annotations

from typing import Iterator

import numpy as np
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models.embeddings import JobEmbedding, TalentEmbedding
from app.repositories import vector_repo


@pytest.fixture
def db_session() -> Iterator[Session]:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(
        engine,
        tables=[
            TalentEmbedding.__table__,
            JobEmbedding.__table__,
        ],
    )
    SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)
    with SessionLocal() as session:
        yield session


def _unit(dim: int, index: int) -> list[float]:
    vec = np.zeros(dim, dtype=np.float32)
    vec[index] = 1.0
    return vec.tolist()


def test_load_talent_vectors_returns_numpy_arrays(db_session: Session) -> None:
    with db_session.begin():
        db_session.add(
            TalentEmbedding(
                talent_id=1,
                model="test",
                dim=4,
                vector_roles={"embedding": _unit(4, 0)},
                vector_skills={"embedding": _unit(4, 1)},
            )
        )

    vectors = vector_repo.load_talent_vectors(db_session, 1)
    assert vectors is not None
    assert isinstance(vectors["roles"], np.ndarray)
    assert np.allclose(vectors["roles"], _unit(4, 0))
    assert np.allclose(vectors["growth"], np.zeros(4, dtype=np.float32))


def test_load_talent_vectors_bulk_skips_missing(db_session: Session) -> None:
    with db_session.begin():
        db_session.add(
            TalentEmbedding(
                talent_id=5,
                model="test",
                dim=3,
                vector_roles={"embedding": _unit(3, 0)},
            )
        )

    results = vector_repo.load_talent_vectors_bulk(db_session, [5, 6])
    assert [item["talent_id"] for item in results] == [5]


def test_list_talent_ids_reflects_embeddings(db_session: Session) -> None:
    with db_session.begin():
        db_session.add(
            TalentEmbedding(
                talent_id=7,
                model="test",
                dim=3,
                vector_roles={"embedding": _unit(3, 0)},
            )
        )
        db_session.add(
            TalentEmbedding(
                talent_id=8,
                model="test",
                dim=3,
                vector_skills={"embedding": _unit(3, 1)},
            )
        )

    ids = vector_repo.list_talent_ids(db_session)
    assert ids == [7, 8]


def test_job_embeddings_loading(db_session: Session) -> None:
    with db_session.begin():
        db_session.add(
            JobEmbedding(
                job_id=11,
                model="test",
                dim=3,
                vector_roles={"embedding": _unit(3, 2)},
            )
        )

    vectors = vector_repo.load_job_vectors(db_session, 11)
    assert vectors is not None
    assert np.allclose(vectors["roles"], _unit(3, 2))


def test_list_job_ids(db_session: Session) -> None:
    with db_session.begin():
        db_session.add(
            JobEmbedding(
                job_id=21,
                model="test",
                dim=3,
                vector_roles={"embedding": _unit(3, 0)},
            )
        )
        db_session.add(
            JobEmbedding(
                job_id=22,
                model="test",
                dim=3,
                vector_skills={"embedding": _unit(3, 1)},
            )
        )

    ids = vector_repo.list_job_ids(db_session)
    assert ids == [21, 22]
