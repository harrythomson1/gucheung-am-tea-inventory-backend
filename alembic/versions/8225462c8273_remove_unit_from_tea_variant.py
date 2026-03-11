"""remove unit from tea variant

Revision ID: 8225462c8273
Revises: 7a3c4a819203
Create Date: 2026-03-12 08:25:52.959072

"""

from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "8225462c8273"
down_revision: str | Sequence[str] | None = "7a3c4a819203"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column("tea_variants", "unit")
    op.execute("DROP TYPE unit")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("CREATE TYPE unit AS ENUM ('grams', 'bags')")
    op.add_column(
        "tea_variants",
        sa.Column(
            "unit", postgresql.ENUM("grams", "bags", name="unit"), nullable=False
        ),
    )
