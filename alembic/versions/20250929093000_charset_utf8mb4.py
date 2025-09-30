"""Ensure utf8mb4 charset and collation across DB and tables

Revision ID: 20250929093000
Revises: 20240927120000
Create Date: 2025-09-29 09:30:00

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "20250929093000"
down_revision = "20240927120000"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    # Get current database name to alter explicitly
    dbname = bind.exec_driver_sql("SELECT DATABASE()").scalar()
    if dbname:
        op.execute(
            f"ALTER DATABASE `{dbname}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )

    # Convert all relevant tables to utf8mb4
    tables = [
        "users",
        "talent_profiles",
        "company_profiles",
        "educations",
        "experiences",
        "activities",
        "certifications",
        "documents",
    ]
    for t in tables:
        op.execute(
            f"ALTER TABLE `{t}` CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )

    # Re-define ENUM with explicit utf8mb4 to be safe for Korean values
    op.execute(
        """
        ALTER TABLE `educations`
        MODIFY `status` ENUM('재학','졸업','휴학','수료','중퇴')
        CHARACTER SET utf8mb4 NOT NULL
        """
    )


def downgrade() -> None:
    # No-op: reverting charset changes is destructive and not recommended.
    # This migration is intended to be one-way to ensure Unicode safety.
    pass

