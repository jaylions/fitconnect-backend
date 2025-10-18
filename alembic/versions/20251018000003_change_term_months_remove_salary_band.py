"""change term_months to text and remove salary_band

Revision ID: 20251018000003
Revises: 20251018000002
Create Date: 2025-10-18 00:00:03.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from sqlalchemy.dialects import mysql


# revision identifiers, used by Alembic.
revision: str = '20251018000003'
down_revision: Union[str, None] = '20251018000002'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def column_exists(connection, table_name: str, column_name: str) -> bool:
    """Check if a column exists in a table"""
    result = connection.execute(text(
        f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS "
        f"WHERE TABLE_SCHEMA = DATABASE() "
        f"AND TABLE_NAME = '{table_name}' "
        f"AND COLUMN_NAME = '{column_name}'"
    ))
    return result.scalar() > 0


def upgrade() -> None:
    connection = op.get_bind()
    
    # Check if old column exists (fresh migration) or new column exists (partial migration)
    old_col_exists = column_exists(connection, 'job_postings', 'term_months')
    new_col_exists = column_exists(connection, 'job_postings', 'term_months_new')
    salary_band_exists = column_exists(connection, 'job_postings', 'salary_band')
    
    # Step 1: Add new term_months_new column as TEXT (if it doesn't exist)
    if not new_col_exists and old_col_exists:
        op.add_column('job_postings', sa.Column('term_months_new', sa.Text(), nullable=True))
        
        # Step 2: Convert existing integer data to text (e.g., 12 -> "12개월")
        op.execute("""
            UPDATE job_postings 
            SET term_months_new = CONCAT(term_months, '개월')
            WHERE term_months IS NOT NULL
        """)
        
        # Step 3: Drop old term_months column (SmallInteger)
        op.drop_column('job_postings', 'term_months')
    
    # Step 4: Rename term_months_new to term_months (if _new column exists)
    if new_col_exists:
        op.execute("ALTER TABLE job_postings CHANGE COLUMN term_months_new term_months TEXT NULL")
    
    # Step 5: Drop salary_band column (JSON) if it exists
    if salary_band_exists:
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
    op.execute("ALTER TABLE job_postings CHANGE COLUMN term_months_int term_months SMALLINT NULL")
