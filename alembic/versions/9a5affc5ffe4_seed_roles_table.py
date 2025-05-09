from alembic import op
import sqlalchemy as sa
import uuid
from datetime import datetime
from typing import Union

# revision identifiers, used by Alembic.
revision: str = '9a5affc5ffe4'
down_revision: Union[str, None] = '847f9fc66ec6'
branch_labels = None
depends_on = None


def upgrade():
    roles_table = sa.table('roles',
        sa.column('id', sa.String(length=512)),
        sa.column('role_name', sa.String(length=50)),
        sa.column('permission', sa.JSON),
        sa.column('created_at', sa.DateTime),
        sa.column('updated_at', sa.DateTime),
    )

    op.bulk_insert(roles_table, [
        {
            'id': str(uuid.uuid4()),
            'role_name': 'Admin',
            'permission': {"can_manage_users": True},
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        },
        {
            'id': str(uuid.uuid4()),
            'role_name': 'Employee',
            'permission': {"can_manage_users": False},
            'created_at': datetime.now(),
            'updated_at': datetime.now(),
        }
    ])


def downgrade():
    op.execute("DELETE FROM roles WHERE role_name IN ('Admin', 'Employee')")
