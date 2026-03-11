"""add weight grams to tea variant

Revision ID: 1de217ff273a
Revises: 8225462c8273
Create Date: 2026-03-12 08:40:05.093156

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "1de217ff273a"
down_revision: str | Sequence[str] | None = "8225462c8273"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "tea_variants",
        sa.Column("weight_grams", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("tea_variants", "weight_grams")
