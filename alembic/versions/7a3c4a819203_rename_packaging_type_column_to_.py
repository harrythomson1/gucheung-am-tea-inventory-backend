"""rename packaging_type column to packaging

Revision ID: 7a3c4a819203
Revises: 17b152fac61b
Create Date: 2026-03-11 13:34:41.291817

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7a3c4a819203"
down_revision: str | Sequence[str] | None = "17b152fac61b"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column("tea_variants", "packaging_type", new_column_name="packaging")


def downgrade() -> None:
    op.alter_column("tea_variants", "packaging", new_column_name="packaging_type")
    # ### end Alembic commands ###
