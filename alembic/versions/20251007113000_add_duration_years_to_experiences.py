"""add duration_years to experiences

Revision ID: 20251007113000
Revises: 20251007100000
Create Date: 2025-10-07 11:30:00.000000
"""

from __future__ import annotations

from datetime import date

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251007113000"
down_revision = "20251007100000"
branch_labels = None
depends_on = None


experiences = sa.table(
    "experiences",
    sa.column("id", sa.BigInteger),
    sa.column("start_ym", sa.Date),
    sa.column("end_ym", sa.Date),
    sa.column("duration_years", sa.Integer),
)


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
    op.add_column("experiences", sa.Column("duration_years", sa.Integer(), nullable=True))

    bind = op.get_bind()
    rows = bind.execute(sa.select(experiences.c.id, experiences.c.start_ym, experiences.c.end_ym)).all()
    for row in rows:
        duration_years = _calculate_duration_years(row.start_ym, row.end_ym)
        if duration_years is not None:
            bind.execute(
                sa.update(experiences)
                .where(experiences.c.id == row.id)
                .values(duration_years=duration_years)
            )


def downgrade() -> None:
    op.drop_column("experiences", "duration_years")

