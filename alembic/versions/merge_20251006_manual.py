"""merge heads after Feat/talent (manual)

Revision ID: 93a65f10cc3a_manual
Revises: 20251003110000, 20251006001500
Create Date: 2025-10-06 01:45:00
"""
from alembic import op  # noqa: F401
import sqlalchemy as sa  # noqa: F401

# revision identifiers, used by Alembic.
revision = "93a65f10cc3a_manual"
down_revision = ("20251003110000", "20251006001500")
branch_labels = None
depends_on = None

def upgrade():
    # pure merge revision (no-op)
    pass

def downgrade():
    # pure merge revision (no-op)
    pass
