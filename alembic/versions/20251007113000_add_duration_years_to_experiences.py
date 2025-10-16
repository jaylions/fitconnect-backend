"""add duration_years to experiences

Revision ID: 20251007113000
Revises: 20251007100000
Create Date: 2025-10-07 11:30:00.000000
"""

from __future__ import annotations

from datetime import date

from alembic import op
import sqlalchemy as sa

# x-args (e.g., `alembic -x duration_batch_size=500 upgrade head`)
_ctx = op.get_context()
x_args = _ctx.get_x_argument(as_dictionary=True) if hasattr(_ctx, "get_x_argument") else {}

# revision identifiers, used by Alembic.
revision = "20251007113000"
down_revision = "20251007100000"
branch_labels = None
depends_on = None


# lightweight table for DML
experiences = sa.table(
    "experiences",
    sa.column("id", sa.BigInteger),
    sa.column("start_ym", sa.Date),
    sa.column("end_ym", sa.Date),
    sa.column("duration_years", sa.Integer),
)


def _has_column(table_name: str, column_name: str) -> bool:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    cols = [c["name"] for c in insp.get_columns(table_name)]
    return column_name in cols


def _calculate_duration_years(start_ym: date | None, end_ym: date | None) -> int | None:
    if start_ym is None:
        return None

    effective_end = end_ym or date.today()
    if effective_end < start_ym:
        return 0

    months = (effective_end.year - start_ym.year) * 12 + (effective_end.month - start_ym.month)
    if effective_end.day < start_ym.day:
        months -= 1

    if months < 0:
        months = 0

    return months // 12


def upgrade() -> None:
    # 1) add column (idempotent)
    if not _has_column("experiences", "duration_years"):
        op.add_column("experiences", sa.Column("duration_years", sa.Integer(), nullable=True))

    # 2) batch size (optional via -x)
    default_batch_size = 1000
    batch_size = default_batch_size
    try:
        if isinstance(x_args, dict) and "duration_batch_size" in x_args:
            batch_size = int(x_args["duration_batch_size"])
    except (TypeError, ValueError):
        batch_size = default_batch_size
    if batch_size < 1:
        batch_size = default_batch_size

    # 3) compute & update
    select_stmt = (
        sa.select(experiences.c.id, experiences.c.start_ym, experiences.c.end_ym)
        .order_by(experiences.c.id)
    )
    update_stmt = (
        sa.update(experiences)
        .where(experiences.c.id == sa.bindparam("pk"))
        .values(duration_years=sa.bindparam("duration_years"))
    )

    connection = op.get_bind().execution_options(stream_results=True)
    result = connection.execute(select_stmt)
    while True:
        rows = result.fetchmany(batch_size)
        if not rows:
            break

        payload = []
        for row in rows:
            duration_years = _calculate_duration_years(row.start_ym, row.end_ym)
            if duration_years is None:
                continue
            payload.append({"pk": row.id, "duration_years": duration_years})

        if payload:
            connection.execute(update_stmt, payload)


def downgrade() -> None:
    if _has_column("experiences", "duration_years"):
        op.drop_column("experiences", "duration_years")