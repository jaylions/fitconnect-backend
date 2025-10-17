"""update job_posting enums and fields

Revision ID: 20251017000000
Revises: 20251008100000
Create Date: 2025-10-17 00:00:00

"""
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

try:  # pragma: no cover - environment-dependent import
    from sqlalchemy.dialects.mysql import JSON as MySQLJSON
    JSONType = MySQLJSON
except ImportError:  # pragma: no cover - fallback for non-MySQL dialects
    JSONType = sa.Text


# revision identifiers, used by Alembic.
revision = "20251017000000"
down_revision = "20251008100000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    Changes:
    1. Add salary_range column to job_postings (nullable, ENUM type)
    2. Alter location_city column type from Text to ENUM
    3. Alter competencies column type from JSON to Text
    """
    
    # Step 1: Add salary_range column (nullable)
    op.add_column(
        'job_postings',
        sa.Column('salary_range', sa.Enum(
            'NEGOTIABLE', 'RANGE_20_30', 'RANGE_30_40', 'RANGE_40_50',
            'RANGE_50_60', 'RANGE_60_70', 'RANGE_70_80', 'RANGE_80_90',
            'RANGE_90_100', 'RANGE_100_120', 'RANGE_120_150', 'OVER_150',
            name='salary_range'
        ), nullable=True)
    )
    
    # Step 2: Alter location_city - convert Text to Enum
    # Add a temporary column with enum type
    op.execute("""
        ALTER TABLE job_postings 
        ADD COLUMN location_city_new ENUM(
            'SEOUL', 'GYEONGGI', 'INCHEON', 'BUSAN', 'DAEGU', 
            'DAEJEON', 'GWANGJU', 'ULSAN', 'GANGWON', 'CHUNGBUK', 
            'CHUNGNAM', 'JEONBUK', 'JEONNAM', 'GYEONGBUK', 'GYEONGNAM'
        ) DEFAULT NULL
    """)
    
    # Migrate existing data - map common values
    op.execute("""
        UPDATE job_postings 
        SET location_city_new = CASE 
            WHEN location_city LIKE '%서울%' OR location_city LIKE '%Seoul%' THEN 'SEOUL'
            WHEN location_city LIKE '%경기%' OR location_city LIKE '%Gyeonggi%' THEN 'GYEONGGI'
            WHEN location_city LIKE '%인천%' OR location_city LIKE '%Incheon%' THEN 'INCHEON'
            WHEN location_city LIKE '%부산%' OR location_city LIKE '%Busan%' THEN 'BUSAN'
            WHEN location_city LIKE '%대구%' OR location_city LIKE '%Daegu%' THEN 'DAEGU'
            WHEN location_city LIKE '%대전%' OR location_city LIKE '%Daejeon%' THEN 'DAEJEON'
            WHEN location_city LIKE '%광주%' OR location_city LIKE '%Gwangju%' THEN 'GWANGJU'
            WHEN location_city LIKE '%울산%' OR location_city LIKE '%Ulsan%' THEN 'ULSAN'
            WHEN location_city LIKE '%강원%' OR location_city LIKE '%Gangwon%' THEN 'GANGWON'
            WHEN location_city LIKE '%충북%' OR location_city LIKE '%Chungbuk%' THEN 'CHUNGBUK'
            WHEN location_city LIKE '%충남%' OR location_city LIKE '%Chungnam%' THEN 'CHUNGNAM'
            WHEN location_city LIKE '%전북%' OR location_city LIKE '%Jeonbuk%' THEN 'JEONBUK'
            WHEN location_city LIKE '%전남%' OR location_city LIKE '%Jeonnam%' THEN 'JEONNAM'
            WHEN location_city LIKE '%경북%' OR location_city LIKE '%Gyeongbuk%' THEN 'GYEONGBUK'
            WHEN location_city LIKE '%경남%' OR location_city LIKE '%Gyeongnam%' THEN 'GYEONGNAM'
            ELSE 'SEOUL'  -- Default fallback
        END
    """)
    
    # Drop old column and rename new one
    op.drop_column('job_postings', 'location_city')
    op.execute("""
        ALTER TABLE job_postings 
        CHANGE location_city_new location_city 
        ENUM('SEOUL', 'GYEONGGI', 'INCHEON', 'BUSAN', 'DAEGU', 
             'DAEJEON', 'GWANGJU', 'ULSAN', 'GANGWON', 'CHUNGBUK', 
             'CHUNGNAM', 'JEONBUK', 'JEONNAM', 'GYEONGBUK', 'GYEONGNAM') NOT NULL
    """)
    
    # Step 3: Alter competencies from JSON to Text
    op.execute("ALTER TABLE job_postings MODIFY COLUMN competencies TEXT NULL")


def downgrade() -> None:
    """Revert changes"""
    
    # Revert competencies back to JSON
    op.execute("ALTER TABLE job_postings MODIFY COLUMN competencies JSON NULL")
    
    # Revert location_city back to Text
    op.execute("ALTER TABLE job_postings ADD COLUMN location_city_old TEXT")
    op.execute("""
        UPDATE job_postings 
        SET location_city_old = CASE location_city
            WHEN 'SEOUL' THEN '서울'
            WHEN 'GYEONGGI' THEN '경기'
            WHEN 'INCHEON' THEN '인천'
            WHEN 'BUSAN' THEN '부산'
            WHEN 'DAEGU' THEN '대구'
            WHEN 'DAEJEON' THEN '대전'
            WHEN 'GWANGJU' THEN '광주'
            WHEN 'ULSAN' THEN '울산'
            WHEN 'GANGWON' THEN '강원'
            WHEN 'CHUNGBUK' THEN '충북'
            WHEN 'CHUNGNAM' THEN '충남'
            WHEN 'JEONBUK' THEN '전북'
            WHEN 'JEONNAM' THEN '전남'
            WHEN 'GYEONGBUK' THEN '경북'
            WHEN 'GYEONGNAM' THEN '경남'
        END
    """)
    op.drop_column('job_postings', 'location_city')
    op.execute("ALTER TABLE job_postings CHANGE location_city_old location_city TEXT NOT NULL")
    
    # Drop salary_range column
    op.drop_column('job_postings', 'salary_range')

