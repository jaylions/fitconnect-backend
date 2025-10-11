"""allow multiple job posting cards per posting

Revision ID: 20251007100000
Revises: 20251007090500
Create Date: 2025-10-07 10:00:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251007100000"
down_revision = "20251007090500"
branch_labels = None
depends_on = None


def _drop_unique_constraints() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    unique_constraints = inspector.get_unique_constraints("job_posting_cards")
    for constraint in unique_constraints:
        column_names = set(constraint.get("column_names") or [])
        if column_names == {"job_posting_id"}:
            op.drop_constraint(constraint["name"], "job_posting_cards", type_="unique")

    indexes = inspector.get_indexes("job_posting_cards")
    for index in indexes:
        if index.get("unique") and index.get("column_names") == ["job_posting_id"]:
            op.drop_index(index["name"], table_name="job_posting_cards")


def upgrade() -> None:
    _drop_unique_constraints()


def downgrade() -> None:
    op.create_unique_constraint(
        "uq_job_posting_cards_job_posting_id",
        "job_posting_cards",
        ["job_posting_id"],
    )
