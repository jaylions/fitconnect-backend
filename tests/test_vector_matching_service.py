from __future__ import annotations

from datetime import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.base import Base
from app.models.matching_vector import MatchingVector
from app.models.user import User
from app.services import vector_matching_service


@pytest.fixture()
def db_session() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, future=True)

    with SessionLocal() as session:
        yield session


def _create_user(session: Session, email: str, role: str) -> User:
    user = User(email=email, password_hash="hashed", role=role)
    session.add(user)
    session.flush()
    return user


def _vector_payload(base: float) -> dict[str, dict[str, list[float]]]:
    return {
        "vector_roles": {"vector": [base, base + 1, base + 2]},
        "vector_skills": {"vector": [base + 3, base + 4, base + 5]},
        "vector_growth": {"vector": [base + 6, base + 7, base + 8]},
        "vector_career": {"vector": [base + 9, base + 10, base + 11]},
        "vector_vision": {"vector": [base + 12, base + 13, base + 14]},
        "vector_culture": {"vector": [base + 15, base + 16, base + 17]},
    }


def _create_matching_vector(session: Session, user: User, base: float) -> MatchingVector:
    payload = _vector_payload(base)
    row = MatchingVector(
        user_id=user.id,
        role=user.role,
        updated_at=datetime.utcnow(),
        **payload,  # type: ignore[arg-type]
    )
    session.add(row)
    session.flush()
    session.refresh(row)
    return row


def test_match_success(db_session: Session) -> None:
    talent = _create_user(db_session, "talent@example.com", "talent")
    company = _create_user(db_session, "company@example.com", "company")
    talent_vector = _create_matching_vector(db_session, talent, 1.0)
    company_vector = _create_matching_vector(db_session, company, 1.5)

    result = vector_matching_service.match(db_session, talent_vector.id, company_vector.id)

    assert result["source"]["role"] == "talent"
    assert result["target"]["role"] == "company"
    assert len(result["field_scores"]) == 6
    assert 0 <= result["score"] <= 100
    assert pytest.approx(result["score"]) == result["total_similarity"]
    assert result["field_scores"]["vector_roles"] <= 100


def test_match_blocks_same_role(db_session: Session) -> None:
    talent_a = _create_user(db_session, "talent1@example.com", "talent")
    talent_b = _create_user(db_session, "talent2@example.com", "talent")
    vector_a = _create_matching_vector(db_session, talent_a, 2.0)
    vector_b = _create_matching_vector(db_session, talent_b, 3.0)

    with pytest.raises(HTTPException) as exc_info:
        vector_matching_service.match(db_session, vector_a.id, vector_b.id)

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail["code"] == "ROLE_MISMATCH"


def test_match_requires_all_fields(db_session: Session) -> None:
    talent = _create_user(db_session, "talent3@example.com", "talent")
    company = _create_user(db_session, "company3@example.com", "company")
    talent_vector = _create_matching_vector(db_session, talent, 4.0)
    incomplete_payload = _vector_payload(5.0)
    incomplete_payload["vector_culture"] = None
    company_vector = MatchingVector(
        user_id=company.id,
        role=company.role,
        updated_at=datetime.utcnow(),
        **incomplete_payload,  # type: ignore[arg-type]
    )
    db_session.add(company_vector)
    db_session.flush()
    db_session.refresh(company_vector)

    with pytest.raises(HTTPException) as exc_info:
        vector_matching_service.match(db_session, talent_vector.id, company_vector.id)

    assert exc_info.value.status_code == 422
    assert exc_info.value.detail["code"] == "INCOMPLETE_VECTOR_FIELDS"
