"""add companies and job_postings tables

Revision ID: 20251003090000
Revises: 20250929093000
Create Date: 2025-10-03 09:00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251003090000"
down_revision = "20250929093000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # companies
    op.create_table(
        "companies",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("owner_user_id", sa.BigInteger(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("industry", sa.Text(), nullable=False),
        sa.Column(
            "size",
            sa.Enum(
                "S_1_10",
                "S_11_50",
                "M_51_200",
                "L_201_500",
                "XL_501_1000",
                "ENT_1000P",
                name="company_size",
                native_enum=True,
            ),
            nullable=True,
        ),
        sa.Column("location_city", sa.Text(), nullable=False),
        sa.Column("homepage_url", sa.Text(), nullable=True),
        sa.Column("career_page_url", sa.Text(), nullable=True),
        sa.Column("one_liner", sa.Text(), nullable=True),
        sa.Column("vision_mission", sa.Text(), nullable=True),
        sa.Column("business_domains", sa.Text(), nullable=True),
        sa.Column("ideal_talent", sa.Text(), nullable=True),
        sa.Column("culture", sa.Text(), nullable=True),
        sa.Column("benefits", sa.Text(), nullable=True),
        sa.Column("profile_step", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("is_submitted", sa.SmallInteger(), nullable=False, server_default=sa.text("0")),
        sa.Column("status", sa.String(length=16), nullable=False, server_default=sa.text("'ACTIVE'")),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    # job_postings
    op.create_table(
        "job_postings",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("company_id", sa.BigInteger(), sa.ForeignKey("companies.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("position_group", sa.Text(), nullable=True),
        sa.Column("department", sa.Text(), nullable=True),
        sa.Column(
            "employment_type",
            sa.Enum(
                "FULL_TIME",
                "PART_TIME",
                "CONTRACT",
                "INTERN",
                "TEMP",
                "OTHER",
                name="employment_type",
                native_enum=True,
            ),
            nullable=False,
        ),
        sa.Column("location_city", sa.Text(), nullable=False),
        sa.Column("career_level", sa.Text(), nullable=False),
        sa.Column("education_level", sa.Text(), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("term_months", sa.SmallInteger(), nullable=True),
        sa.Column("homepage_url", sa.Text(), nullable=True),
        sa.Column("deadline_date", sa.Date(), nullable=True),
        sa.Column("contact_email", sa.Text(), nullable=True),
        sa.Column("contact_phone", sa.Text(), nullable=True),
        sa.Column("salary_band", sa.JSON(), nullable=True),
        sa.Column("responsibilities", sa.Text(), nullable=True),
        sa.Column("requirements_must", sa.Text(), nullable=True),
        sa.Column("requirements_nice", sa.Text(), nullable=True),
        sa.Column("competencies", sa.JSON(), nullable=True),
        sa.Column(
            "status",
            sa.Enum("DRAFT", "PUBLISHED", "CLOSED", "ARCHIVED", name="job_posting_status"),
            nullable=False,
            server_default=sa.text("'DRAFT'"),
        ),
        sa.Column("jd_file_id", sa.Text(), nullable=True),
        sa.Column("extra_file_id", sa.Text(), nullable=True),
        sa.Column("published_at", sa.DateTime(), nullable=True),
        sa.Column("closed_at", sa.DateTime(), nullable=True),
        sa.Column("deleted_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
            server_default=sa.text("CURRENT_TIMESTAMP"),
            server_onupdate=sa.text("CURRENT_TIMESTAMP"),
        ),
    )

    op.create_index(
        "ix_job_postings_company_status", "job_postings", ["company_id", "status"], unique=False
    )
    op.create_index("ix_job_postings_status", "job_postings", ["status"], unique=False)
    op.create_index(
        "ix_job_postings_deadline_date", "job_postings", ["deadline_date"], unique=False
    )


def downgrade() -> None:
    op.drop_index("ix_job_postings_deadline_date", table_name="job_postings")
    op.drop_index("ix_job_postings_status", table_name="job_postings")
    op.drop_index("ix_job_postings_company_status", table_name="job_postings")
    op.drop_table("job_postings")
    op.drop_table("companies")
    # Clean up PostgreSQL enum types to avoid "type already exists" on re-run
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        # Enum type names as declared in upgrade()
        op.execute("DROP TYPE IF EXISTS job_posting_status")
        op.execute("DROP TYPE IF EXISTS employment_type")
        op.execute("DROP TYPE IF EXISTS company_size")
