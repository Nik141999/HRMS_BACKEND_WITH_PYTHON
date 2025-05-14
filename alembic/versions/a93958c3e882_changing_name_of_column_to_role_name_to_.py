"""changing name of column to role_name to role_type

Revision ID: a93958c3e882
Revises: aace9e2c3871
Create Date: 2025-05-13 15:49:52.816344

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a93958c3e882'
down_revision: Union[str, None] = 'aace9e2c3871'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
