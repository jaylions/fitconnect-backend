"""drop legacy company_profiles table

Revision ID: 20251003110000
Revises: 20251003090000
Create Date: 2025-10-03 11:00:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251003110000"
down_revision = "20251003090000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Use raw SQL for IF EXISTS safety on MySQL
    op.execute(sa.text("DROP TABLE IF EXISTS `company_profiles`"))


def downgrade() -> None:
    # Recreate legacy table as it was in initial migration
    op.create_table(
        "company_profiles",
        sa.Column("user_id", sa.BigInteger(), sa.ForeignKey("users.id"), primary_key=True),
        sa.Column("company_name", sa.String(length=255), nullable=True),
        sa.Column("industry", sa.String(length=255), nullable=True),
        sa.Column("size", sa.String(length=100), nullable=True),
        sa.Column("location", sa.String(length=255), nullable=True),
        sa.Column("description", sa.String(length=1024), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
    )

