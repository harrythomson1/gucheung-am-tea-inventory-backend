"""add new enum type

Revision ID: dcaae3a41e9d
Revises: 5801f915f81d
Create Date: 2026-04-13 13:35:28.928484

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "dcaae3a41e9d"
down_revision: str | Sequence[str] | None = "5801f915f81d"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TYPE transaction_type ADD VALUE 'repackage'")


def downgrade() -> None:
    """Downgrade schema."""
    pass
