"""make experience title nullable

Revision ID: 20251018000001
Revises: 20251018000000
Create Date: 2025-10-18 00:00:01.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20251018000001'
down_revision: Union[str, None] = '20251018000000'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Make title column nullable in experiences table
    op.alter_column('experiences', 'title',
                    existing_type=sa.String(length=255),
                    nullable=True)


def downgrade() -> None:
    # Make title column not nullable again
    op.alter_column('experiences', 'title',
                    existing_type=sa.String(length=255),
                    nullable=False)
