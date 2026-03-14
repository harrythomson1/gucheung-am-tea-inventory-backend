"""add standard to flush type

Revision ID: a3670b1e2004
Revises: 3d269590d823
Create Date: 2026-03-14 15:45:18.241062

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a3670b1e2004"
down_revision: str | Sequence[str] | None = "3d269590d823"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TYPE packaging_type ADD VALUE 'standard'")


def downgrade() -> None:
    pass
