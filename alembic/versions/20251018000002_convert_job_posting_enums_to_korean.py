"""convert job posting enums to korean values

Revision ID: 20251018000002
Revises: 20251018000001
Create Date: 2025-10-18 00:00:02.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision: str = '20251018000002'
down_revision: Union[str, None] = '20251018000001'
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
    
    # Check if old columns exist (fresh migration) or new columns exist (partial migration)
    old_cols_exist = column_exists(connection, 'job_postings', 'employment_type')
    new_cols_exist = column_exists(connection, 'job_postings', 'employment_type_new')
    
    # Step 1: Add new columns with Korean enum values (if they don't exist)
    if old_cols_exist and not new_cols_exist:
        op.execute("""
            ALTER TABLE job_postings 
            ADD COLUMN employment_type_new ENUM('정규직', '계약직', '파견직', '인턴', '임시직', '기타') NULL
        """)
        
        op.execute("""
            ALTER TABLE job_postings 
            ADD COLUMN location_city_new ENUM('서울', '경기', '인천', '부산', '대구', '대전', '광주', '울산', '강원', '충북', '충남', '전북', '전남', '경북', '경남') NULL
        """)
        
        op.execute("""
            ALTER TABLE job_postings 
            ADD COLUMN salary_range_new ENUM('연봉 추후 협상', '2000만 ~ 3000만', '3000만 ~ 4000만', '4000만 ~ 5000만', '5000만 ~ 6000만', '6000만 ~ 7000만', '7000만 ~ 8000만', '8000만 ~ 9000만', '9000만 ~ 1억', '1억 ~ 1.2억', '1.2억 ~ 1.5억', '1.5억 이상') NULL
        """)
    
    # Step 2: Convert data from English to Korean (only if old columns exist)
    if old_cols_exist:
        # Employment Type
        op.execute("UPDATE job_postings SET employment_type_new = '정규직' WHERE employment_type = 'FULL_TIME'")
        op.execute("UPDATE job_postings SET employment_type_new = '계약직' WHERE employment_type = 'CONTRACT'")
        op.execute("UPDATE job_postings SET employment_type_new = '파견직' WHERE employment_type = 'PART_TIME'")
        op.execute("UPDATE job_postings SET employment_type_new = '인턴' WHERE employment_type = 'INTERN'")
        op.execute("UPDATE job_postings SET employment_type_new = '임시직' WHERE employment_type = 'TEMP'")
        op.execute("UPDATE job_postings SET employment_type_new = '기타' WHERE employment_type = 'OTHER'")
        
        # Location
        op.execute("UPDATE job_postings SET location_city_new = '서울' WHERE location_city = 'SEOUL'")
        op.execute("UPDATE job_postings SET location_city_new = '경기' WHERE location_city = 'GYEONGGI'")
        op.execute("UPDATE job_postings SET location_city_new = '인천' WHERE location_city = 'INCHEON'")
        op.execute("UPDATE job_postings SET location_city_new = '부산' WHERE location_city = 'BUSAN'")
        op.execute("UPDATE job_postings SET location_city_new = '대구' WHERE location_city = 'DAEGU'")
        op.execute("UPDATE job_postings SET location_city_new = '대전' WHERE location_city = 'DAEJEON'")
        op.execute("UPDATE job_postings SET location_city_new = '광주' WHERE location_city = 'GWANGJU'")
        op.execute("UPDATE job_postings SET location_city_new = '울산' WHERE location_city = 'ULSAN'")
        op.execute("UPDATE job_postings SET location_city_new = '강원' WHERE location_city = 'GANGWON'")
        op.execute("UPDATE job_postings SET location_city_new = '충북' WHERE location_city = 'CHUNGBUK'")
        op.execute("UPDATE job_postings SET location_city_new = '충남' WHERE location_city = 'CHUNGNAM'")
        op.execute("UPDATE job_postings SET location_city_new = '전북' WHERE location_city = 'JEONBUK'")
        op.execute("UPDATE job_postings SET location_city_new = '전남' WHERE location_city = 'JEONNAM'")
        op.execute("UPDATE job_postings SET location_city_new = '경북' WHERE location_city = 'GYEONGBUK'")
        op.execute("UPDATE job_postings SET location_city_new = '경남' WHERE location_city = 'GYEONGNAM'")
        
        # Salary Range
        op.execute("UPDATE job_postings SET salary_range_new = '연봉 추후 협상' WHERE salary_range = 'NEGOTIABLE'")
        op.execute("UPDATE job_postings SET salary_range_new = '2000만 ~ 3000만' WHERE salary_range = 'RANGE_20_30'")
        op.execute("UPDATE job_postings SET salary_range_new = '3000만 ~ 4000만' WHERE salary_range = 'RANGE_30_40'")
        op.execute("UPDATE job_postings SET salary_range_new = '4000만 ~ 5000만' WHERE salary_range = 'RANGE_40_50'")
        op.execute("UPDATE job_postings SET salary_range_new = '5000만 ~ 6000만' WHERE salary_range = 'RANGE_50_60'")
        op.execute("UPDATE job_postings SET salary_range_new = '6000만 ~ 7000만' WHERE salary_range = 'RANGE_60_70'")
        op.execute("UPDATE job_postings SET salary_range_new = '7000만 ~ 8000만' WHERE salary_range = 'RANGE_70_80'")
        op.execute("UPDATE job_postings SET salary_range_new = '8000만 ~ 9000만' WHERE salary_range = 'RANGE_80_90'")
        op.execute("UPDATE job_postings SET salary_range_new = '9000만 ~ 1억' WHERE salary_range = 'RANGE_90_100'")
        op.execute("UPDATE job_postings SET salary_range_new = '1억 ~ 1.2억' WHERE salary_range = 'RANGE_100_120'")
        op.execute("UPDATE job_postings SET salary_range_new = '1.2억 ~ 1.5억' WHERE salary_range = 'RANGE_120_150'")
        op.execute("UPDATE job_postings SET salary_range_new = '1.5억 이상' WHERE salary_range = 'OVER_150'")
        
        # Step 3: Drop old columns
        op.drop_column('job_postings', 'employment_type')
        op.drop_column('job_postings', 'location_city')
        op.drop_column('job_postings', 'salary_range')
    
    # Step 4: Rename new columns to original names
    op.execute("ALTER TABLE job_postings CHANGE COLUMN employment_type_new employment_type ENUM('정규직', '계약직', '파견직', '인턴', '임시직', '기타') NULL")
    op.execute("ALTER TABLE job_postings CHANGE COLUMN location_city_new location_city ENUM('서울', '경기', '인천', '부산', '대구', '대전', '광주', '울산', '강원', '충북', '충남', '전북', '전남', '경북', '경남') NULL")
    op.execute("ALTER TABLE job_postings CHANGE COLUMN salary_range_new salary_range ENUM('연봉 추후 협상', '2000만 ~ 3000만', '3000만 ~ 4000만', '4000만 ~ 5000만', '5000만 ~ 6000만', '6000만 ~ 7000만', '7000만 ~ 8000만', '8000만 ~ 9000만', '9000만 ~ 1억', '1억 ~ 1.2억', '1.2억 ~ 1.5억', '1.5억 이상') NULL")
    
    # Step 5: Make employment_type and location_city NOT NULL
    op.execute("ALTER TABLE job_postings MODIFY COLUMN employment_type ENUM('정규직', '계약직', '파견직', '인턴', '임시직', '기타') NOT NULL")
    op.execute("ALTER TABLE job_postings MODIFY COLUMN location_city ENUM('서울', '경기', '인천', '부산', '대구', '대전', '광주', '울산', '강원', '충북', '충남', '전북', '전남', '경북', '경남') NOT NULL")


def downgrade() -> None:
    # Reverse the process
    # Step 1: Add old columns back
    op.execute("""
        ALTER TABLE job_postings 
        ADD COLUMN employment_type_old ENUM('FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERN', 'TEMP', 'OTHER') NULL
    """)
    
    op.execute("""
        ALTER TABLE job_postings 
        ADD COLUMN location_city_old ENUM('SEOUL', 'GYEONGGI', 'INCHEON', 'BUSAN', 'DAEGU', 'DAEJEON', 'GWANGJU', 'ULSAN', 'GANGWON', 'CHUNGBUK', 'CHUNGNAM', 'JEONBUK', 'JEONNAM', 'GYEONGBUK', 'GYEONGNAM') NULL
    """)
    
    op.execute("""
        ALTER TABLE job_postings 
        ADD COLUMN salary_range_old ENUM('NEGOTIABLE', 'RANGE_20_30', 'RANGE_30_40', 'RANGE_40_50', 'RANGE_50_60', 'RANGE_60_70', 'RANGE_70_80', 'RANGE_80_90', 'RANGE_90_100', 'RANGE_100_120', 'RANGE_120_150', 'OVER_150') NULL
    """)
    
    # Step 2: Convert back to English
    op.execute("UPDATE job_postings SET employment_type_old = 'FULL_TIME' WHERE employment_type = '정규직'")
    op.execute("UPDATE job_postings SET employment_type_old = 'CONTRACT' WHERE employment_type = '계약직'")
    op.execute("UPDATE job_postings SET employment_type_old = 'PART_TIME' WHERE employment_type = '파견직'")
    op.execute("UPDATE job_postings SET employment_type_old = 'INTERN' WHERE employment_type = '인턴'")
    op.execute("UPDATE job_postings SET employment_type_old = 'TEMP' WHERE employment_type = '임시직'")
    op.execute("UPDATE job_postings SET employment_type_old = 'OTHER' WHERE employment_type = '기타'")
    
    op.execute("UPDATE job_postings SET location_city_old = 'SEOUL' WHERE location_city = '서울'")
    op.execute("UPDATE job_postings SET location_city_old = 'GYEONGGI' WHERE location_city = '경기'")
    op.execute("UPDATE job_postings SET location_city_old = 'INCHEON' WHERE location_city = '인천'")
    op.execute("UPDATE job_postings SET location_city_old = 'BUSAN' WHERE location_city = '부산'")
    op.execute("UPDATE job_postings SET location_city_old = 'DAEGU' WHERE location_city = '대구'")
    op.execute("UPDATE job_postings SET location_city_old = 'DAEJEON' WHERE location_city = '대전'")
    op.execute("UPDATE job_postings SET location_city_old = 'GWANGJU' WHERE location_city = '광주'")
    op.execute("UPDATE job_postings SET location_city_old = 'ULSAN' WHERE location_city = '울산'")
    op.execute("UPDATE job_postings SET location_city_old = 'GANGWON' WHERE location_city = '강원'")
    op.execute("UPDATE job_postings SET location_city_old = 'CHUNGBUK' WHERE location_city = '충북'")
    op.execute("UPDATE job_postings SET location_city_old = 'CHUNGNAM' WHERE location_city = '충남'")
    op.execute("UPDATE job_postings SET location_city_old = 'JEONBUK' WHERE location_city = '전북'")
    op.execute("UPDATE job_postings SET location_city_old = 'JEONNAM' WHERE location_city = '전남'")
    op.execute("UPDATE job_postings SET location_city_old = 'GYEONGBUK' WHERE location_city = '경북'")
    op.execute("UPDATE job_postings SET location_city_old = 'GYEONGNAM' WHERE location_city = '경남'")
    
    op.execute("UPDATE job_postings SET salary_range_old = 'NEGOTIABLE' WHERE salary_range = '연봉 추후 협상'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_20_30' WHERE salary_range = '2000만 ~ 3000만'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_30_40' WHERE salary_range = '3000만 ~ 4000만'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_40_50' WHERE salary_range = '4000만 ~ 5000만'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_50_60' WHERE salary_range = '5000만 ~ 6000만'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_60_70' WHERE salary_range = '6000만 ~ 7000만'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_70_80' WHERE salary_range = '7000만 ~ 8000만'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_80_90' WHERE salary_range = '8000만 ~ 9000만'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_90_100' WHERE salary_range = '9000만 ~ 1억'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_100_120' WHERE salary_range = '1억 ~ 1.2억'")
    op.execute("UPDATE job_postings SET salary_range_old = 'RANGE_120_150' WHERE salary_range = '1.2억 ~ 1.5억'")
    op.execute("UPDATE job_postings SET salary_range_old = 'OVER_150' WHERE salary_range = '1.5억 이상'")
    
    # Step 3: Drop Korean columns
    op.drop_column('job_postings', 'employment_type')
    op.drop_column('job_postings', 'location_city')
    op.drop_column('job_postings', 'salary_range')
    
    # Step 4: Rename old columns back
    op.execute("ALTER TABLE job_postings CHANGE COLUMN employment_type_old employment_type ENUM('FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERN', 'TEMP', 'OTHER') NULL")
    op.execute("ALTER TABLE job_postings CHANGE COLUMN location_city_old location_city ENUM('SEOUL', 'GYEONGGI', 'INCHEON', 'BUSAN', 'DAEGU', 'DAEJEON', 'GWANGJU', 'ULSAN', 'GANGWON', 'CHUNGBUK', 'CHUNGNAM', 'JEONBUK', 'JEONNAM', 'GYEONGBUK', 'GYEONGNAM') NULL")
    op.execute("ALTER TABLE job_postings CHANGE COLUMN salary_range_old salary_range ENUM('NEGOTIABLE', 'RANGE_20_30', 'RANGE_30_40', 'RANGE_40_50', 'RANGE_50_60', 'RANGE_60_70', 'RANGE_70_80', 'RANGE_80_90', 'RANGE_90_100', 'RANGE_100_120', 'RANGE_120_150', 'OVER_150') NULL")
    
    # Step 5: Make employment_type and location_city NOT NULL
    op.execute("ALTER TABLE job_postings MODIFY COLUMN employment_type ENUM('FULL_TIME', 'PART_TIME', 'CONTRACT', 'INTERN', 'TEMP', 'OTHER') NOT NULL")
    op.execute("ALTER TABLE job_postings MODIFY COLUMN location_city ENUM('SEOUL', 'GYEONGGI', 'INCHEON', 'BUSAN', 'DAEGU', 'DAEJEON', 'GWANGJU', 'ULSAN', 'GANGWON', 'CHUNGBUK', 'CHUNGNAM', 'JEONBUK', 'JEONNAM', 'GYEONGBUK', 'GYEONGNAM') NOT NULL")
