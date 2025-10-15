from sqlalchemy import inspect

from app.db.base import Base
from app.models.embeddings import JobEmbedding, TalentEmbedding


def test_talent_embedding_columns():
    mapper = inspect(TalentEmbedding)
    column_keys = {column.key for column in mapper.columns}
    expected = {
        "talent_id",
        "model",
        "dim",
        "vector_roles",
        "vector_skills",
        "vector_growth",
        "vector_career",
        "vector_vision",
        "vector_culture",
        "updated_at",
    }
    assert expected.issubset(column_keys)


def test_job_embedding_columns():
    mapper = inspect(JobEmbedding)
    column_keys = {column.key for column in mapper.columns}
    expected = {
        "job_id",
        "model",
        "dim",
        "vector_roles",
        "vector_skills",
        "vector_growth",
        "vector_career",
        "vector_vision",
        "vector_culture",
        "updated_at",
    }
    assert expected.issubset(column_keys)


def test_metadata_contains_embedding_tables():
    tables = Base.metadata.tables
    assert "talent_embeddings" in tables
    assert "job_embeddings" in tables
