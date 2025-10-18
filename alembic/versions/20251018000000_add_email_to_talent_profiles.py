"""add email to talent_profiles

Revision ID: 20251018000000
Revises: 20251017000000
Create Date: 2025-10-18 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20251018000000'
down_revision: Union[str, None] = '20251017000000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add email column to talent_profiles table
    op.add_column('talent_profiles', sa.Column('email', sa.String(length=255), nullable=True))


def downgrade() -> None:
    # Remove email column from talent_profiles table
    op.drop_column('talent_profiles', 'email')
