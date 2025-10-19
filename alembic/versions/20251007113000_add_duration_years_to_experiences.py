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

# lightweight table for DML
experiences = sa.table(
    "experiences",
    sa.column("id", sa.BigInteger),
    sa.column("start_ym", sa.Date),
    sa.column("end_ym", sa.Date),
    sa.column("duration_years", sa.Integer),
)

def _has_column(table_name: str, column_name: str) -> bool:
    conn = op.get_bind()
    insp = sa.inspect(conn)
    cols = [c["name"] for c in insp.get_columns(table_name)]
    return column_name in cols

def upgrade() -> None:
    conn = op.get_bind()

    # 1️⃣ 컬럼 없을 때만 추가
    if not _has_column("experiences", "duration_years"):
        op.add_column("experiences", sa.Column("duration_years", sa.Integer, nullable=True))

    # 2️⃣ 기존 행에 대해 duration_years 계산
    rows = list(conn.execute(sa.select(experiences.c.id, experiences.c.start_ym, experiences.c.end_ym)))
    for row in rows:
        start, end = row.start_ym, row.end_ym
        if start and end:
            years = (end.year - start.year) + (end.month - start.month) / 12.0
            years_int = int(round(years))
            conn.execute(
                experiences.update()
                .where(experiences.c.id == row.id)
                .values(duration_years=years_int)
            )

def downgrade() -> None:
    if _has_column("experiences", "duration_years"):
        op.drop_column("experiences", "duration_years")