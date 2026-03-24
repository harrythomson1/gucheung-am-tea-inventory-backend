"""add unique constraints

Revision ID: c8fc8565c980
Revises: 63dd22914e65
Create Date: 2026-03-25 08:44:35.696843

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "c8fc8565c980"
down_revision: str | Sequence[str] | None = "63dd22914e65"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_unique_constraint("uq_teas_name", "teas", ["name"])
    op.create_unique_constraint(
        "uq_tea_variant",
        "tea_variants",
        ["tea_id", "packaging", "flush", "harvest_year", "weight_grams"],
    )


def downgrade() -> None:
    op.drop_constraint("uq_tea_variant", "tea_variants")
    op.drop_constraint("uq_teas_name", "teas")
