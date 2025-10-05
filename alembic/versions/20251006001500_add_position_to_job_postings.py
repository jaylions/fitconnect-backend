"""add position column to job_postings

Revision ID: 20251006001500
Revises: 20251005094500
Create Date: 2025-10-06 00:15:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251006001500"
down_revision = "20251005094500"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("job_postings", sa.Column("position", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("job_postings", "position")

