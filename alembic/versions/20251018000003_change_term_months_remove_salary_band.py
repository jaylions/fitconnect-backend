"""change term_months to text and remove salary_band

Revision ID: 20251018000003
Revises: 20251018000002
Create Date: 2025-10-18 00:00:03.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = '20251018000003'
down_revision: Union[str, None] = '20251018000002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Step 1: Add new term_months_new column as TEXT
    op.add_column('job_postings', sa.Column('term_months_new', sa.Text(), nullable=True))
    
    # Step 2: Convert existing integer data to text (e.g., 12 -> "12개월")
    op.execute("""
        UPDATE job_postings 
        SET term_months_new = CONCAT(term_months, '개월')
        WHERE term_months IS NOT NULL
    """)
    
    # Step 3: Drop old term_months column (SmallInteger)
    op.drop_column('job_postings', 'term_months')
    
    # Step 4: Rename term_months_new to term_months
    op.alter_column('job_postings', 'term_months_new', new_column_name='term_months')
    
    # Step 5: Drop salary_band column (JSON)
    op.drop_column('job_postings', 'salary_band')


def downgrade() -> None:
    # Step 1: Add salary_band column back
    op.add_column('job_postings', sa.Column('salary_band', mysql.JSON(), nullable=True))
    
    # Step 2: Add new term_months_int column as SmallInteger
    op.add_column('job_postings', sa.Column('term_months_int', sa.SmallInteger(), nullable=True))
    
    # Step 3: Try to extract integer from text (e.g., "12개월" -> 12)
    op.execute("""
        UPDATE job_postings 
        SET term_months_int = CAST(REGEXP_REPLACE(term_months, '[^0-9]', '') AS SIGNED)
        WHERE term_months IS NOT NULL AND term_months REGEXP '[0-9]+'
    """)
    
    # Step 4: Drop text term_months column
    op.drop_column('job_postings', 'term_months')
    
    # Step 5: Rename term_months_int to term_months
    op.alter_column('job_postings', 'term_months_int', new_column_name='term_months')
