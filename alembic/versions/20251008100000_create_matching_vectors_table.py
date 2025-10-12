"""create matching_vectors table

Revision ID: 20251008100000
Revises: 20251007113000
Create Date: 2025-10-08 10:00:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

try:  # pragma: no cover - environment-dependent import
    from sqlalchemy.dialects.mysql import JSON as MySQLJSON

    JSONType = MySQLJSON
except ImportError:  # pragma: no cover - fallback for non-MySQL dialects
    JSONType = sa.Text


# revision identifiers, used by Alembic.
revision = "20251008100000"
down_revision = "20251007113000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "matching_vectors",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "role",
            sa.Enum("talent", "company", name="matching_vector_role"),
            nullable=False,
        ),
        sa.Column("vector_roles", JSONType(), nullable=True),
        sa.Column("vector_skills", JSONType(), nullable=True),
        sa.Column("vector_growth", JSONType(), nullable=True),
        sa.Column("vector_career", JSONType(), nullable=True),
        sa.Column("vector_vision", JSONType(), nullable=True),
        sa.Column("vector_culture", JSONType(), nullable=True),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
    )
    op.create_index("ix_matching_vectors_user_id", "matching_vectors", ["user_id"])
    op.create_index("ix_matching_vectors_role", "matching_vectors", ["role"])


def downgrade() -> None:
    op.drop_index("ix_matching_vectors_role", table_name="matching_vectors")
    op.drop_index("ix_matching_vectors_user_id", table_name="matching_vectors")
    op.drop_table("matching_vectors")

