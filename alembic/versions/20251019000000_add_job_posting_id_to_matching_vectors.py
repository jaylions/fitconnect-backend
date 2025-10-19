"""add job_posting_id to matching_vectors

Revision ID: 20251019000000
Revises: 20251018000003
Create Date: 2025-10-19 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20251019000000'
down_revision = '20251018000003'
branch_labels = None
depends_on = None


def upgrade():
    # 1. job_posting_id 컬럼 추가 (nullable)
    op.add_column(
        'matching_vectors',
        sa.Column('job_posting_id', sa.BigInteger(), nullable=True)
    )
    
    # 2. job_postings 테이블에 대한 외래 키 추가
    op.create_foreign_key(
        'fk_matching_vectors_job_posting_id',
        'matching_vectors',
        'job_postings',
        ['job_posting_id'],
        ['id'],
        ondelete='CASCADE'
    )
    
    # 3. job_posting_id에 인덱스 추가
    op.create_index(
        'ix_matching_vectors_job_posting_id',
        'matching_vectors',
        ['job_posting_id']
    )
    
    # 4. 기존 unique constraint 삭제 (있다면)
    # Note: MySQL에서는 constraint 이름이 필요함
    # 기존에 unique constraint가 없다면 이 부분은 주석 처리
    
    # 5. 새로운 unique constraint 추가
    # user_id + job_posting_id 조합이 unique (talent는 job_posting_id=NULL이므로 user_id만으로 unique)
    op.create_unique_constraint(
        'uq_matching_vector_user_jobposting',
        'matching_vectors',
        ['user_id', 'job_posting_id']
    )


def downgrade():
    # 1. unique constraint 제거
    op.drop_constraint('uq_matching_vector_user_jobposting', 'matching_vectors', type_='unique')
    
    # 2. 인덱스 제거
    op.drop_index('ix_matching_vectors_job_posting_id', 'matching_vectors')
    
    # 3. 외래 키 제거
    op.drop_constraint('fk_matching_vectors_job_posting_id', 'matching_vectors', type_='foreignkey')
    
    # 4. 컬럼 제거
    op.drop_column('matching_vectors', 'job_posting_id')
