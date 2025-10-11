"""create job_posting_cards and talent_cards tables

Revision ID: 20251007090000
Revises: 20251006001500
Create Date: 2025-10-07 09:00:00

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
revision = "20251007090000"
down_revision = "20251006001500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "job_posting_cards",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "job_posting_id",
            sa.BigInteger(),
            sa.ForeignKey("job_postings.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("header_title", sa.String(length=100), nullable=True),
        sa.Column("badge_role", sa.String(length=100), nullable=True),
        sa.Column("deadline_date", sa.Date(), nullable=True),
        sa.Column("headline", sa.String(length=255), nullable=True),
        sa.Column("posting_info", JSONType(), nullable=True),
        sa.Column("responsibilities", JSONType(), nullable=True),
        sa.Column("requirements", JSONType(), nullable=True),
        sa.Column("required_competencies", JSONType(), nullable=True),
        sa.Column("company_info", sa.Text(), nullable=True),
        sa.Column("talent_persona", sa.Text(), nullable=True),
        sa.Column("challenge_task", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.UniqueConstraint("job_posting_id", name="uq_job_posting_cards_job_posting_id"),
    )

    op.create_table(
        "talent_cards",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            unique=True,
        ),
        sa.Column("header_title", sa.String(length=100), nullable=True),
        sa.Column("badge_title", sa.String(length=120), nullable=True),
        sa.Column("badge_years", sa.Integer(), nullable=True),
        sa.Column("badge_employment", sa.String(length=120), nullable=True),
        sa.Column("headline", sa.String(length=255), nullable=True),
        sa.Column("experiences", JSONType(), nullable=True),
        sa.Column("strengths", JSONType(), nullable=True),
        sa.Column("general_capabilities", JSONType(), nullable=True),
        sa.Column("job_skills", JSONType(), nullable=True),
        sa.Column("performance_summary", sa.Text(), nullable=True),
        sa.Column("collaboration_style", sa.Text(), nullable=True),
        sa.Column("growth_potential", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
        sa.UniqueConstraint("user_id", name="uq_talent_cards_user_id"),
    )


def downgrade() -> None:
    op.drop_table("talent_cards")
    op.drop_table("job_posting_cards")
