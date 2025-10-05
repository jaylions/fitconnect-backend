"""update company_size enum to Korean labels

Revision ID: 20251005094500
Revises: 20251005093000
Create Date: 2025-10-05 09:45:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "20251005094500"
down_revision = "20251005093000"
branch_labels = None
depends_on = None


# Old -> New mapping
OLD_TO_NEW = {
    "S_1_10": "1 ~ 10명",
    "S_11_50": "10 ~ 50명",
    "M_51_200": "100 ~ 200명",  # ambiguous; choose upper bucket by default
    "L_201_500": "200 ~ 500명",
    "XL_501_1000": "500 ~ 1000명",
    "ENT_1000P": "1000명 이상",
}

NEW_VALUES = [
    "1 ~ 10명",
    "10 ~ 50명",
    "50 ~ 100명",
    "100 ~ 200명",
    "200 ~ 500명",
    "500 ~ 1000명",
    "1000명 이상",
]

OLD_VALUES = [
    "S_1_10",
    "S_11_50",
    "M_51_200",
    "L_201_500",
    "XL_501_1000",
    "ENT_1000P",
]


def upgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        op.execute("ALTER TYPE company_size RENAME TO company_size_old")
        op.execute(
            "CREATE TYPE company_size AS ENUM ('" + "','".join(NEW_VALUES) + "')"
        )
        # Map old codes to new labels
        op.execute(
            """
            ALTER TABLE companies
            ALTER COLUMN size TYPE company_size
            USING (
                CASE
                    WHEN size::text = 'S_1_10' THEN '1 ~ 10명'::company_size
                    WHEN size::text = 'S_11_50' THEN '10 ~ 50명'::company_size
                    WHEN size::text = 'M_51_200' THEN '100 ~ 200명'::company_size
                    WHEN size::text = 'L_201_500' THEN '200 ~ 500명'::company_size
                    WHEN size::text = 'XL_501_1000' THEN '500 ~ 1000명'::company_size
                    WHEN size::text = 'ENT_1000P' THEN '1000명 이상'::company_size
                    ELSE NULL
                END
            )
            """
        )
        op.execute("DROP TYPE company_size_old")

    elif dialect == "mysql":
        # Temporarily allow both old and new values
        op.execute(
            "ALTER TABLE companies MODIFY COLUMN size "
            "ENUM('S_1_10','S_11_50','M_51_200','L_201_500','XL_501_1000','ENT_1000P',"
            "'1 ~ 10명','10 ~ 50명','50 ~ 100명','100 ~ 200명','200 ~ 500명','500 ~ 1000명','1000명 이상')"
            " NULL"
        )
        # Map data
        for old, new in OLD_TO_NEW.items():
            op.execute(
                sa.text("UPDATE companies SET size=:new WHERE size=:old").bindparams(new=new, old=old)
            )
        # Restrict to only new values
        op.execute(
            "ALTER TABLE companies MODIFY COLUMN size "
            "ENUM('1 ~ 10명','10 ~ 50명','50 ~ 100명','100 ~ 200명','200 ~ 500명','500 ~ 1000명','1000명 이상') NULL"
        )

    else:
        enum_type = sa.Enum(*NEW_VALUES, name="company_size")
        enum_type.create(bind, checkfirst=True)
        op.alter_column(
            "companies",
            "size",
            type_=enum_type,
            existing_nullable=True,
        )


def downgrade() -> None:
    bind = op.get_bind()
    dialect = bind.dialect.name

    if dialect == "postgresql":
        op.execute("ALTER TYPE company_size RENAME TO company_size_new")
        op.execute(
            "CREATE TYPE company_size AS ENUM ('" + "','".join(OLD_VALUES) + "')"
        )
        op.execute(
            """
            ALTER TABLE companies
            ALTER COLUMN size TYPE company_size
            USING (
                CASE
                    WHEN size::text = '1 ~ 10명' THEN 'S_1_10'::company_size
                    WHEN size::text = '10 ~ 50명' THEN 'S_11_50'::company_size
                    WHEN size::text IN ('50 ~ 100명','100 ~ 200명') THEN 'M_51_200'::company_size
                    WHEN size::text = '200 ~ 500명' THEN 'L_201_500'::company_size
                    WHEN size::text = '500 ~ 1000명' THEN 'XL_501_1000'::company_size
                    WHEN size::text = '1000명 이상' THEN 'ENT_1000P'::company_size
                    ELSE NULL
                END
            )
            """
        )
        op.execute("DROP TYPE company_size_new")

    elif dialect == "mysql":
        # Allow both sets, map back, then restrict
        op.execute(
            "ALTER TABLE companies MODIFY COLUMN size "
            "ENUM('S_1_10','S_11_50','M_51_200','L_201_500','XL_501_1000','ENT_1000P',"
            "'1 ~ 10명','10 ~ 50명','50 ~ 100명','100 ~ 200명','200 ~ 500명','500 ~ 1000명','1000명 이상')"
            " NULL"
        )
        # Map new back to old (compress 50~100 and 100~200 into M_51_200)
        op.execute("UPDATE companies SET size='S_1_10' WHERE size='1 ~ 10명'")
        op.execute("UPDATE companies SET size='S_11_50' WHERE size='10 ~ 50명'")
        op.execute("UPDATE companies SET size='M_51_200' WHERE size IN ('50 ~ 100명','100 ~ 200명')")
        op.execute("UPDATE companies SET size='L_201_500' WHERE size='200 ~ 500명'")
        op.execute("UPDATE companies SET size='XL_501_1000' WHERE size='500 ~ 1000명'")
        op.execute("UPDATE companies SET size='ENT_1000P' WHERE size='1000명 이상'")
        op.execute(
            "ALTER TABLE companies MODIFY COLUMN size "
            "ENUM('S_1_10','S_11_50','M_51_200','L_201_500','XL_501_1000','ENT_1000P') NULL"
        )

    else:
        enum_type = sa.Enum(*OLD_VALUES, name="company_size")
        enum_type.create(bind, checkfirst=True)
        op.alter_column(
            "companies",
            "size",
            type_=enum_type,
            existing_nullable=True,
        )

