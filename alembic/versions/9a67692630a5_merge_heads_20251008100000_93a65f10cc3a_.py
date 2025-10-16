"""merge heads: 20251008100000 + 93a65f10cc3a_manual

Revision ID: 9a67692630a5
Revises: 20251008100000, 93a65f10cc3a_manual
Create Date: 2025-10-16 12:17:45.530430

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '9a67692630a5'
down_revision = ('20251008100000', '93a65f10cc3a_manual')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

