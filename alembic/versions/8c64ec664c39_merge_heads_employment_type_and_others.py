"""merge heads employment_type and others

Revision ID: 8c64ec664c39
Revises: 20251025125518, a0dfdd14243b
Create Date: 2025-10-25 12:56:15.529330

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '8c64ec664c39'
down_revision = ('20251025125518', 'a0dfdd14243b')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

