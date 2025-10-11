"""allow multiple job posting cards per posting

Revision ID: 20251007100000
Revises: 20251007090500
Create Date: 2025-10-07 10:00:00

"""
from __future__ import annotations

import sqlalchemy as sa
from alembic import op
from sqlalchemy import exc as sa_exc


# revision identifiers, used by Alembic.
revision = "20251007100000"
down_revision = "20251007090500"
branch_labels = None
depends_on = None


def _get_inspector() -> sa.Inspector:
    inspector = sa.inspect(op.get_bind())
    info_cache = getattr(inspector, "info_cache", None)
    if isinstance(info_cache, dict):
        info_cache.clear()
    return inspector


def _drop_foreign_keys_to_job_postings(table_name: str = "job_posting_cards") -> list[str]:
    inspector = _get_inspector()
    dropped: list[str] = []
    target_name = "fk_job_posting_cards_job_posting_id"
    target_columns = ["job_posting_id"]

    for fk in inspector.get_foreign_keys(table_name):
        fk_name = fk.get("name")
        constrained_columns = fk.get("constrained_columns") or []
        if fk.get("referred_table") != "job_postings":
            continue

        if fk_name not in {target_name, None} and constrained_columns != target_columns:
            continue

        if fk_name:
            op.drop_constraint(fk_name, table_name, type_="foreignkey")
            dropped.append(fk_name)

    return dropped


def _drop_unique_constraint_or_index(
    table_name: str, constraint_name: str
) -> None:
    inspector = _get_inspector()
    unique_names = {uc["name"] for uc in inspector.get_unique_constraints(table_name)}
    index_names = {idx["name"] for idx in inspector.get_indexes(table_name)}

    if constraint_name not in unique_names and constraint_name not in index_names:
        return

    try:
        with op.batch_alter_table(table_name) as batch_op:
            batch_op.drop_constraint(constraint_name, type_="unique")
        return
    except (sa_exc.DBAPIError, sa_exc.OperationalError, NotImplementedError):
        pass

    with op.batch_alter_table(table_name) as batch_op:
        try:
            batch_op.drop_index(constraint_name)
        except (sa_exc.DBAPIError, sa_exc.OperationalError):
            inspector = _get_inspector()
            still_exists = any(
                constraint_name == uc["name"]
                for uc in inspector.get_unique_constraints(table_name)
            ) or any(
                constraint_name == idx["name"]
                for idx in inspector.get_indexes(table_name)
            )
            if still_exists:
                raise


def _ensure_index(
    table_name: str, index_name: str, columns: list[str]
) -> None:
    inspector = _get_inspector()
    if any(idx["name"] == index_name for idx in inspector.get_indexes(table_name)):
        return

    with op.batch_alter_table(table_name) as batch_op:
        batch_op.create_index(index_name, columns)


def _drop_index_if_exists(table_name: str, index_name: str) -> None:
    inspector = _get_inspector()
    if not any(idx["name"] == index_name for idx in inspector.get_indexes(table_name)):
        return

    with op.batch_alter_table(table_name) as batch_op:
        batch_op.drop_index(index_name)


def _ensure_unique_constraint(
    table_name: str, constraint_name: str, columns: list[str]
) -> None:
    inspector = _get_inspector()
    if any(uc["name"] == constraint_name for uc in inspector.get_unique_constraints(table_name)):
        return

    with op.batch_alter_table(table_name) as batch_op:
        batch_op.create_unique_constraint(constraint_name, columns)


def _ensure_foreign_key(
    table_name: str,
    constraint_name: str,
    referred_table: str,
    local_columns: list[str],
    remote_columns: list[str],
    **options: object,
) -> None:
    inspector = _get_inspector()
    for fk in inspector.get_foreign_keys(table_name):
        if fk.get("name") == constraint_name:
            return

    op.create_foreign_key(
        constraint_name,
        table_name,
        referred_table,
        local_columns,
        remote_columns,
        **options,
    )


def upgrade() -> None:
    _drop_foreign_keys_to_job_postings()
    _drop_unique_constraint_or_index("job_posting_cards", "uq_job_posting_cards_job_posting_id")
    _ensure_index("job_posting_cards", "ix_job_posting_cards_job_posting_id", ["job_posting_id"])
    _ensure_foreign_key(
        "job_posting_cards",
        "fk_job_posting_cards_job_posting_id",
        "job_postings",
        ["job_posting_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    _drop_foreign_keys_to_job_postings()
    _drop_index_if_exists("job_posting_cards", "ix_job_posting_cards_job_posting_id")
    _ensure_unique_constraint(
        "job_posting_cards",
        "uq_job_posting_cards_job_posting_id",
        ["job_posting_id"],
    )
    _ensure_foreign_key(
        "job_posting_cards",
        "fk_job_posting_cards_job_posting_id",
        "job_postings",
        ["job_posting_id"],
        ["id"],
    )
