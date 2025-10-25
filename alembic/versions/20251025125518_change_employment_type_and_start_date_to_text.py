"""change employment_type and start_date to text

Revision ID: 20251025125518
Revises: 20251018000003
Create Date: 2025-10-25 12:55:18

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '20251025125518'
down_revision = '20251018000003'
branch_labels = None
depends_on = None


def upgrade():
    # 1. employment_type을 ENUM에서 TEXT로 변경
    # MySQL의 경우 직접 ALTER TABLE로 변경
    op.execute("""
        ALTER TABLE job_postings 
        MODIFY COLUMN employment_type TEXT NOT NULL
    """)
    
    # 2. start_date를 DATE에서 TEXT로 변경
    op.execute("""
        ALTER TABLE job_postings 
        MODIFY COLUMN start_date TEXT NULL
    """)


def downgrade():
    # 다운그레이드 시 다시 원래 타입으로 복원
    # 주의: 데이터 손실 가능성이 있으므로 신중하게 사용
    
    # start_date를 TEXT에서 DATE로 복원
    op.execute("""
        ALTER TABLE job_postings 
        MODIFY COLUMN start_date DATE NULL
    """)
    
    # employment_type을 TEXT에서 ENUM으로 복원
    op.execute("""
        ALTER TABLE job_postings 
        MODIFY COLUMN employment_type ENUM('정규직', '계약직', '파견직', '인턴', '임시직', '기타') NOT NULL
    """)
