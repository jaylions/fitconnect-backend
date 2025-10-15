"""add talent and job embedding tables with optional legacy backfill

Revision ID: 20251009110000
Revises: 20251008100000
Create Date: 2025-10-09 11:00:00
"""

from __future__ import annotations

from collections.abc import Iterable
import json
import math
import os
from typing import Any

import sqlalchemy as sa
from alembic import op
from sqlalchemy import inspect
from sqlalchemy.dialects import mysql
from sqlalchemy.engine import Connection
from sqlalchemy.engine.reflection import Inspector

# revision identifiers, used by Alembic.
revision = "20251009110000"
down_revision = "20251008100000"
branch_labels = None
depends_on = None

DEFAULT_MODEL = "text-embedding-3-small"
DEFAULT_DIM = 1536


def _get_inspector(connection: Connection) -> Inspector:
    inspector = inspect(connection)
    info_cache = getattr(inspector, "info_cache", None)
    if isinstance(info_cache, dict):
        info_cache.clear()
    return inspector


def _table_exists(inspector: Inspector, table_name: str) -> bool:
    return table_name in inspector.get_table_names()


def _column_exists(inspector: Inspector, table_name: str, column_name: str) -> bool:
    try:
        return any(col["name"] == column_name for col in inspector.get_columns(table_name))
    except sa.exc.NoSuchTableError:
        return False


def _view_exists(connection: Connection, view_name: str) -> bool:
    inspector = _get_inspector(connection)
    schema = inspector.default_schema_name or None
    try:
        view_names = inspector.get_view_names(schema=schema)
    except TypeError:
        view_names = inspector.get_view_names()
    except NotImplementedError:
        view_names = inspector.get_view_names()
    return view_name in set(view_names)


def _json_type(connection: Connection) -> sa.types.TypeEngine[Any]:
    if connection.dialect.name == "mysql":
        return mysql.JSON()
    return sa.JSON()


def _parse_vector_payload(value: Any) -> dict[str, list[float]] | None:
    if value is None:
        return None
    payload: Any = value
    if isinstance(payload, bytes):
        payload = payload.decode("utf-8")
    if isinstance(payload, str):
        payload = payload.strip()
        if not payload:
            return None
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return None

    if isinstance(payload, dict):
        data = payload.get("embedding")
        if data is None and len(payload) == 1:
            data = next(iter(payload.values()))
    elif isinstance(payload, Iterable) and not isinstance(payload, (str, bytes)):
        data = list(payload)
    else:
        return None

    if data is None:
        return None

    if isinstance(data, bytes):
        try:
            data = json.loads(data.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None

    if isinstance(data, str):
        try:
            data = json.loads(data)
        except json.JSONDecodeError:
            return None

    if not isinstance(data, Iterable) or isinstance(data, (str, bytes)):
        return None

    vector = []
    for item in data:
        try:
            number = float(item)
        except (TypeError, ValueError):
            return None
        if math.isnan(number) or math.isinf(number):
            return None
        vector.append(number)

    if not vector:
        return None

    if len(vector) != DEFAULT_DIM:
        return None

    norm = math.sqrt(sum(component * component for component in vector))
    if not norm:
        return None

    if not math.isclose(norm, 1.0, rel_tol=1e-2, abs_tol=1e-2):
        return None

    return {"embedding": vector}


def _collect_legacy_talent_vectors(connection: Connection, inspector: Inspector) -> dict[int, dict[str, dict[str, list[float]]]]:
    vectors: dict[int, dict[str, dict[str, list[float]]]] = {}

    if _table_exists(inspector, "matching_vectors"):
        stmt = sa.text(
            "SELECT user_id, vector_roles, vector_skills, vector_growth, "
            "vector_career, vector_vision, vector_culture "
            "FROM matching_vectors WHERE role = 'talent'"
        )
        for row in connection.execute(stmt):
            user_id = int(row.user_id)
            facet_map = vectors.setdefault(user_id, {})
            for facet in ("vector_roles", "vector_skills", "vector_growth", "vector_career", "vector_vision", "vector_culture"):
                parsed = _parse_vector_payload(getattr(row, facet))
                if parsed is not None:
                    vectors[user_id][facet] = parsed

    for legacy_column in ("matching_vector", "matching_vectors"):
        if not _column_exists(inspector, "talent_profiles", legacy_column):
            continue
        stmt = sa.text(
            f"SELECT user_id, {legacy_column} AS payload "
            "FROM talent_profiles "
            "WHERE {legacy_column} IS NOT NULL".format(legacy_column=legacy_column)
        )
        for row in connection.execute(stmt):
            user_id = int(row.user_id)
            parsed = _parse_vector_payload(row.payload)
            if parsed is None:
                continue
            facet_map = vectors.setdefault(user_id, {})
            facet_map.setdefault("vector_roles", parsed)

    return vectors


def _collect_legacy_job_vectors(connection: Connection, inspector: Inspector) -> dict[int, dict[str, dict[str, list[float]]]]:
    vectors: dict[int, dict[str, dict[str, list[float]]]] = {}

    for legacy_column in ("matching_vector", "matching_vectors"):
        if not _column_exists(inspector, "job_postings", legacy_column):
            continue
        stmt = sa.text(
            f"SELECT id AS job_id, {legacy_column} AS payload "
            "FROM job_postings "
            f"WHERE {legacy_column} IS NOT NULL"
        )
        for row in connection.execute(stmt):
            job_id = int(row.job_id)
            parsed = _parse_vector_payload(row.payload)
            if parsed is None:
                continue
            facet_map = vectors.setdefault(job_id, {})
            facet_map.setdefault("vector_roles", parsed)

    return vectors


def _backfill_embeddings(connection: Connection, inspector: Inspector) -> None:
    if os.getenv("ENABLE_BACKFILL", "").lower() not in {"1", "true", "yes"}:
        return

    talent_table = sa.table(
        "talent_embeddings",
        sa.column("talent_id", sa.BigInteger()),
        sa.column("model", sa.String(64)),
        sa.column("dim", sa.SmallInteger()),
        sa.column("vector_roles", sa.JSON()),
        sa.column("vector_skills", sa.JSON()),
        sa.column("vector_growth", sa.JSON()),
        sa.column("vector_career", sa.JSON()),
        sa.column("vector_vision", sa.JSON()),
        sa.column("vector_culture", sa.JSON()),
    )
    job_table = sa.table(
        "job_embeddings",
        sa.column("job_id", sa.BigInteger()),
        sa.column("model", sa.String(64)),
        sa.column("dim", sa.SmallInteger()),
        sa.column("vector_roles", sa.JSON()),
        sa.column("vector_skills", sa.JSON()),
        sa.column("vector_growth", sa.JSON()),
        sa.column("vector_career", sa.JSON()),
        sa.column("vector_vision", sa.JSON()),
        sa.column("vector_culture", sa.JSON()),
    )

    if _table_exists(inspector, "talent_embeddings"):
        legacy_vectors = _collect_legacy_talent_vectors(connection, inspector)
        payload = []
        for talent_id, facets in legacy_vectors.items():
            if not facets:
                continue
            row = {
                "talent_id": talent_id,
                "model": DEFAULT_MODEL,
                "dim": DEFAULT_DIM,
            }
            row.update(facets)
            payload.append(row)
        if payload:
            insert_stmt = sa.insert(talent_table)
            if connection.dialect.name == "mysql":
                insert_stmt = insert_stmt.prefix_with("IGNORE")
            connection.execute(insert_stmt, payload)

    if _table_exists(inspector, "job_embeddings"):
        legacy_vectors = _collect_legacy_job_vectors(connection, inspector)
        payload = []
        for job_id, facets in legacy_vectors.items():
            if not facets:
                continue
            row = {
                "job_id": job_id,
                "model": DEFAULT_MODEL,
                "dim": DEFAULT_DIM,
            }
            row.update(facets)
            payload.append(row)
        if payload:
            insert_stmt = sa.insert(job_table)
            if connection.dialect.name == "mysql":
                insert_stmt = insert_stmt.prefix_with("IGNORE")
            connection.execute(insert_stmt, payload)


def upgrade() -> None:
    connection = op.get_bind()
    inspector = _get_inspector(connection)
    json_type = _json_type(connection)
    json_constructor = "JSON_OBJECT" if connection.dialect.name == "mysql" else "json_build_object"

    if not _table_exists(inspector, "talent_embeddings"):
        op.create_table(
            "talent_embeddings",
            sa.Column(
                "talent_id",
                sa.BigInteger(),
                sa.ForeignKey("talent_profiles.user_id", ondelete="CASCADE"),
                primary_key=True,
            ),
            sa.Column("model", sa.String(length=64), nullable=False),
            sa.Column("dim", sa.SmallInteger(), nullable=False),
            sa.Column("vector_roles", json_type, nullable=True),
            sa.Column("vector_skills", json_type, nullable=True),
            sa.Column("vector_growth", json_type, nullable=True),
            sa.Column("vector_career", json_type, nullable=True),
            sa.Column("vector_vision", json_type, nullable=True),
            sa.Column("vector_culture", json_type, nullable=True),
            sa.Column(
                "updated_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                server_onupdate=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
            mysql_engine="InnoDB",
        )

    inspector = _get_inspector(connection)

    if not _table_exists(inspector, "job_embeddings"):
        op.create_table(
            "job_embeddings",
            sa.Column(
                "job_id",
                sa.BigInteger(),
                sa.ForeignKey("job_postings.id", ondelete="CASCADE"),
                primary_key=True,
            ),
            sa.Column("model", sa.String(length=64), nullable=False),
            sa.Column("dim", sa.SmallInteger(), nullable=False),
            sa.Column("vector_roles", json_type, nullable=True),
            sa.Column("vector_skills", json_type, nullable=True),
            sa.Column("vector_growth", json_type, nullable=True),
            sa.Column("vector_career", json_type, nullable=True),
            sa.Column("vector_vision", json_type, nullable=True),
            sa.Column("vector_culture", json_type, nullable=True),
            sa.Column(
                "updated_at",
                sa.DateTime(),
                server_default=sa.text("CURRENT_TIMESTAMP"),
                server_onupdate=sa.text("CURRENT_TIMESTAMP"),
                nullable=False,
            ),
            mysql_engine="InnoDB",
        )

    inspector = _get_inspector(connection)

    if _table_exists(inspector, "talent_embeddings") and not _view_exists(connection, "talent_matching_vector_view"):
        op.execute(
            sa.text(
                f"""
                CREATE VIEW talent_matching_vector_view AS
                SELECT
                    tp.user_id AS talent_id,
                    {json_constructor}(
                        'roles', te.vector_roles,
                        'skills', te.vector_skills,
                        'growth', te.vector_growth,
                        'career', te.vector_career,
                        'vision', te.vector_vision,
                        'culture', te.vector_culture
                    ) AS matching_vector
                FROM talent_profiles tp
                LEFT JOIN talent_embeddings te ON te.talent_id = tp.user_id
                """
            )
        )

    inspector = _get_inspector(connection)

    if _table_exists(inspector, "job_embeddings") and not _view_exists(connection, "job_matching_vector_view"):
        op.execute(
            sa.text(
                f"""
                CREATE VIEW job_matching_vector_view AS
                SELECT
                    jp.id AS job_id,
                    {json_constructor}(
                        'roles', je.vector_roles,
                        'skills', je.vector_skills,
                        'growth', je.vector_growth,
                        'career', je.vector_career,
                        'vision', je.vector_vision,
                        'culture', je.vector_culture
                    ) AS matching_vector
                FROM job_postings jp
                LEFT JOIN job_embeddings je ON je.job_id = jp.id
                """
            )
        )

    inspector = _get_inspector(connection)
    _backfill_embeddings(connection, inspector)


def downgrade() -> None:
    connection = op.get_bind()
    inspector = _get_inspector(connection)

    op.execute(sa.text("DROP VIEW IF EXISTS job_matching_vector_view"))
    op.execute(sa.text("DROP VIEW IF EXISTS talent_matching_vector_view"))

    if _table_exists(inspector, "job_embeddings"):
        op.drop_table("job_embeddings")

    inspector = _get_inspector(connection)

    if _table_exists(inspector, "talent_embeddings"):
        op.drop_table("talent_embeddings")
