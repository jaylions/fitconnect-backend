"""merge heads 2025-10-11 unify after allow_multiple_cards

Revision ID: e03be39550e4
Revises: 5e6ce5c0c73c, 20251007100000
Create Date: 2025-10-11 06:52:51.997619

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'e03be39550e4'
down_revision = ('5e6ce5c0c73c', '20251007100000')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

