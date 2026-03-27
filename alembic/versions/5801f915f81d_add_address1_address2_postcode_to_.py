"""add address1 address2 postcode to customers

Revision ID: 5801f915f81d
Revises: bc96e7482f80
Create Date: 2026-03-27 14:15:06.706494

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5801f915f81d"
down_revision: str | Sequence[str] | None = "bc96e7482f80"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("customers", sa.Column("address_1", sa.String(), nullable=True))
    op.add_column("customers", sa.Column("address_2", sa.String(), nullable=True))
    op.add_column("customers", sa.Column("postcode", sa.String(), nullable=True))
    op.drop_column("customers", "address")


def downgrade() -> None:
    op.add_column("customers", sa.Column("address", sa.String(), nullable=True))
    op.drop_column("customers", "postcode")
    op.drop_column("customers", "address_2")
    op.drop_column("customers", "address_1")
