"""empty message

Revision ID: 68d2e18da73a
Revises: e273259847c5
Create Date: 2024-02-17 20:30:57.692093

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '68d2e18da73a'
down_revision: Union[str, None] = 'e273259847c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
