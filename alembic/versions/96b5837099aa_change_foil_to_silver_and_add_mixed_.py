"""change foil to silver and add mixed packaging type

Revision ID: 96b5837099aa
Revises: 1de217ff273a
Create Date: 2026-03-12 10:14:20.243562

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "96b5837099aa"
down_revision: str | Sequence[str] | None = "1de217ff273a"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("ALTER TYPE packaging_type RENAME VALUE 'foil' TO 'silver'")
    op.execute("ALTER TYPE packaging_type ADD VALUE 'mixed'")


def downgrade() -> None:
    pass
