"""drop organization and organization_type tables

Revision ID: 2f7aa5a14086
Revises: e63b91f61a3e
Create Date: 2025-06-18 11:43:24.129746

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f7aa5a14086'
down_revision: Union[str, None] = 'e63b91f61a3e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_table('organizations')
    op.drop_table('organization_type')

def downgrade():
    # Optional: recreate the tables here if needed
    pass