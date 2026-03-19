"""add customer table and update stock transactions

Revision ID: 2d78d136ab50
Revises: a3670b1e2004
Create Date: 2026-03-19 10:03:44.273164

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2d78d136ab50"
down_revision: str | Sequence[str] | None = "a3670b1e2004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "customers",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("city", sa.String(), nullable=False),
        sa.Column("address", sa.String(), nullable=True),
        sa.Column("phone", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "stock_transactions", sa.Column("customer_id", sa.Integer(), nullable=True)
    )
    op.create_foreign_key(
        "stock_transactions_customer_id_fkey",
        "stock_transactions",
        "customers",
        ["customer_id"],
        ["id"],
    )
    op.drop_column("stock_transactions", "buyer_name")
    op.drop_column("stock_transactions", "buyer_phone")


def downgrade() -> None:
    op.add_column(
        "stock_transactions", sa.Column("buyer_name", sa.String(), nullable=True)
    )
    op.add_column(
        "stock_transactions", sa.Column("buyer_phone", sa.String(), nullable=True)
    )
    op.drop_constraint("stock_transactions_customer_id_fkey", "stock_transactions")
    op.drop_column("stock_transactions", "customer_id")
    op.drop_table("customers")
