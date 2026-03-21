"""add deleted column to teas table

Revision ID: 63dd22914e65
Revises: 8295a90939bf
Create Date: 2026-03-21 14:00:28.256478

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "63dd22914e65"
down_revision: str | Sequence[str] | None = "8295a90939bf"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "teas",
        sa.Column("deleted", sa.Boolean(), server_default="false", nullable=False),
    )


def downgrade() -> None:
    op.drop_column("teas", "deleted")
