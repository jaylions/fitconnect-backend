"""update education_status enum values

Revision ID: 20251005093000
Revises: 20251003090000
Create Date: 2025-10-05 09:30:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251005093000"
down_revision = "20251003090000"
branch_labels = None
depends_on = None


NEW_VALUES = ["재학", "휴학", "졸업 예정", "졸업 유예", "졸업", "중퇴"]
OLD_VALUES = ["재학", "졸업", "휴학", "수료", "중퇴"]


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        # Rename old type, create new, convert values (수료 -> 졸업 유예), drop old
        op.execute("ALTER TYPE education_status RENAME TO education_status_old")
        op.execute(
            "CREATE TYPE education_status AS ENUM ('" + "','".join(NEW_VALUES) + "')"
        )
        op.execute(
            """
            ALTER TABLE educations
            ALTER COLUMN status TYPE education_status
            USING (
                CASE
                    WHEN status::text = '수료' THEN '졸업 유예'::education_status
                    ELSE status::text::education_status
                END
            )
            """
        )
        op.execute("DROP TYPE education_status_old")

    elif dialect == "mysql":
        # Expand enum to include legacy + new, migrate data, then shrink
        op.execute(
            "ALTER TABLE educations MODIFY COLUMN status "
            "ENUM('재학','휴학','졸업 예정','졸업 유예','졸업','중퇴','수료') NOT NULL"
        )
        op.execute("UPDATE educations SET status='졸업 유예' WHERE status='수료'")
        op.execute(
            "ALTER TABLE educations MODIFY COLUMN status "
            "ENUM('재학','휴학','졸업 예정','졸업 유예','졸업','중퇴') NOT NULL"
        )

    else:
        # Fallback using SQLAlchemy Enum type where supported
        enum_type = sa.Enum(*NEW_VALUES, name="education_status")
        enum_type.create(bind, checkfirst=True)
        op.alter_column(
            "educations",
            "status",
            type_=enum_type,
            existing_nullable=False,
        )


def downgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        # Create old type, convert values back (졸업 유예 -> 수료, 졸업 예정 -> 재학), drop new
        op.execute("ALTER TYPE education_status RENAME TO education_status_new")
        op.execute(
            "CREATE TYPE education_status AS ENUM ('" + "','".join(OLD_VALUES) + "')"
        )
        op.execute(
            """
            ALTER TABLE educations
            ALTER COLUMN status TYPE education_status
            USING (
                CASE
                    WHEN status::text = '졸업 유예' THEN '수료'::education_status
                    WHEN status::text = '졸업 예정' THEN '재학'::education_status
                    ELSE status::text::education_status
                END
            )
            """
        )
        op.execute("DROP TYPE education_status_new")

    elif dialect == "mysql":
        # Allow both sets, map back, then restrict
        op.execute(
            "ALTER TABLE educations MODIFY COLUMN status "
            "ENUM('재학','졸업','휴학','수료','중퇴','졸업 예정','졸업 유예') NOT NULL"
        )
        op.execute(
            "UPDATE educations SET status='수료' WHERE status='졸업 유예'"
        )
        op.execute(
            "UPDATE educations SET status='재학' WHERE status='졸업 예정'"
        )
        op.execute(
            "ALTER TABLE educations MODIFY COLUMN status "
            "ENUM('재학','졸업','휴학','수료','중퇴') NOT NULL"
        )

    else:
        enum_type = sa.Enum(*OLD_VALUES, name="education_status")
        enum_type.create(bind, checkfirst=True)
        op.alter_column(
            "educations",
            "status",
            type_=enum_type,
            existing_nullable=False,
        )
