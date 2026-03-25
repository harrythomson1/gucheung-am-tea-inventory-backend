"""add updated_at to customers

Revision ID: bc96e7482f80
Revises: c8fc8565c980
Create Date: 2026-03-25 15:23:51.187501

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "bc96e7482f80"
down_revision: str | Sequence[str] | None = "c8fc8565c980"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "customers",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("customers", "updated_at")
