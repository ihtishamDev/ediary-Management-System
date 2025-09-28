"""add phone_number, gender, address to users

Revision ID: f5e25ff8b73a
Revises: bde7b610635c
Create Date: 2025-09-26 10:33:43.132996

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5e25ff8b73a'
down_revision: Union[str, Sequence[str], None] = 'bde7b610635c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True))
    op.add_column('users', sa.Column('gender', sa.String(), nullable=True))
    op.add_column('users', sa.Column('address', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'address')
    op.drop_column('users', 'gender')
    op.drop_column('users', 'phone_number')
