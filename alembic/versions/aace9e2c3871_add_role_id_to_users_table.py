"""Add role_id to users table

Revision ID: aace9e2c3871
Revises: 352e3e92ea6b
Create Date: 2025-05-13 13:50:33.602812

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aace9e2c3871'
down_revision: Union[str, None] = '352e3e92ea6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema by adding 'role_id' column and foreign key constraint"""
    # Add 'role_id' column to 'users' table
    op.add_column('users', sa.Column('role_id', sa.VARCHAR(512), nullable=False))
    
    # Create foreign key constraint linking 'role_id' in 'users' table to 'id' in 'roles' table
    op.create_foreign_key('fk_users_roles', 'users', 'roles', ['role_id'], ['id'])


def downgrade() -> None:
    """Downgrade schema by removing 'role_id' column and foreign key constraint"""
    # Drop foreign key constraint
    op.drop_constraint('fk_users_roles', 'users', type_='foreignkey')
    
    # Drop 'role_id' column from 'users' table
    op.drop_column('users', 'role_id')
