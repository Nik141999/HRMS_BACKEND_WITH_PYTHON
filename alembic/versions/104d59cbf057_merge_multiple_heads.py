"""merge multiple heads

Revision ID: 104d59cbf057
Revises: 60a5c228e455, c7d84dc8491a
Create Date: 2025-05-20 13:15:34.029475

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '104d59cbf057'
down_revision: Union[str, None] = ('60a5c228e455', 'c7d84dc8491a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
