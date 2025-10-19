"""merge heads 2025-10-12 unify branches

Revision ID: a50240eabbfe
Revises: 20251008100000, ed297fa0b80d
Create Date: 2025-10-12 06:35:18.733515

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'a50240eabbfe'
down_revision = ('20251008100000', 'ed297fa0b80d')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

