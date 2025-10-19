"""merge heads after duration_years

Revision ID: 2d7f6702cf22
Revises: 9a67692630a5, a50240eabbfe
Create Date: 2025-10-16 12:26:10.341517

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = '2d7f6702cf22'
down_revision = ('9a67692630a5', 'a50240eabbfe')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

