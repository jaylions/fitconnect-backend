"""create_matching_results_table

Revision ID: d855df47bc1d
Revises: 286882850f0f
Create Date: 2025-10-25 14:44:00.291691

"""
from alembic import op
import sqlalchemy as sa



# revision identifiers, used by Alembic.
revision = 'd855df47bc1d'
down_revision = '286882850f0f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # matching_results 테이블 생성
    op.create_table(
        'matching_results',
        sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
        sa.Column('talent_vector_id', sa.BigInteger(), nullable=False),
        sa.Column('company_vector_id', sa.BigInteger(), nullable=False),
        sa.Column('talent_user_id', sa.BigInteger(), nullable=False),
        sa.Column('company_user_id', sa.BigInteger(), nullable=False),
        sa.Column('job_posting_id', sa.BigInteger(), nullable=False),
        sa.Column('total_score', sa.DECIMAL(5, 2), nullable=False),
        sa.Column('score_roles', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('score_skills', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('score_growth', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('score_career', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('score_vision', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('score_culture', sa.DECIMAL(5, 2), nullable=True),
        sa.Column('calculated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('talent_vector_id', 'company_vector_id', name='uq_matching_pair')
    )
    
    # 인덱스 생성
    op.create_index('ix_matching_results_talent_vector_id', 'matching_results', ['talent_vector_id'])
    op.create_index('ix_matching_results_company_vector_id', 'matching_results', ['company_vector_id'])
    op.create_index('ix_matching_results_talent_user_id', 'matching_results', ['talent_user_id'])
    op.create_index('ix_matching_results_company_user_id', 'matching_results', ['company_user_id'])
    op.create_index('ix_matching_results_job_posting_id', 'matching_results', ['job_posting_id'])
    
    # 외래 키 추가
    op.create_foreign_key(
        'fk_matching_results_talent_vector',
        'matching_results', 'matching_vectors',
        ['talent_vector_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_matching_results_company_vector',
        'matching_results', 'matching_vectors',
        ['company_vector_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_matching_results_talent_user',
        'matching_results', 'users',
        ['talent_user_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_matching_results_company_user',
        'matching_results', 'users',
        ['company_user_id'], ['id'],
        ondelete='CASCADE'
    )
    op.create_foreign_key(
        'fk_matching_results_job_posting',
        'matching_results', 'job_postings',
        ['job_posting_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade() -> None:
    # 외래 키 제거
    op.drop_constraint('fk_matching_results_job_posting', 'matching_results', type_='foreignkey')
    op.drop_constraint('fk_matching_results_company_user', 'matching_results', type_='foreignkey')
    op.drop_constraint('fk_matching_results_talent_user', 'matching_results', type_='foreignkey')
    op.drop_constraint('fk_matching_results_company_vector', 'matching_results', type_='foreignkey')
    op.drop_constraint('fk_matching_results_talent_vector', 'matching_results', type_='foreignkey')
    
    # 인덱스 제거
    op.drop_index('ix_matching_results_job_posting_id', 'matching_results')
    op.drop_index('ix_matching_results_company_user_id', 'matching_results')
    op.drop_index('ix_matching_results_talent_user_id', 'matching_results')
    op.drop_index('ix_matching_results_company_vector_id', 'matching_results')
    op.drop_index('ix_matching_results_talent_vector_id', 'matching_results')
    
    # 테이블 제거
    op.drop_table('matching_results')

