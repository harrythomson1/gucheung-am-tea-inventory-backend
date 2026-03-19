"""add notes to customer tablewq

Revision ID: 8295a90939bf
Revises: 2d78d136ab50
Create Date: 2026-03-19 13:56:23.873676

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8295a90939bf"
down_revision: str | Sequence[str] | None = "2d78d136ab50"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("customers", sa.Column("notes", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("customers", "notes")
