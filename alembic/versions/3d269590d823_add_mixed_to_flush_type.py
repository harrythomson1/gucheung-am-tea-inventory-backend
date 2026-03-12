"""add mixed to flush type

Revision ID: 3d269590d823
Revises: 96b5837099aa
Create Date: 2026-03-12 10:15:57.365811

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3d269590d823"
down_revision: str | Sequence[str] | None = "96b5837099aa"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TYPE flush_type ADD VALUE 'mixed'")


def downgrade() -> None:
    pass
