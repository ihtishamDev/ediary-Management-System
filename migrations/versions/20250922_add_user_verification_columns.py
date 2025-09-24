"""Safely add verification and reset columns to users table"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect

# revision identifiers, used by Alembic.
revision = "20250922_add_user_verification_columns"
down_revision = None  # or set this to the previous migration ID if you have one
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col["name"] for col in inspector.get_columns("users")]

    if "verification_token" not in columns:
        op.add_column("users", sa.Column("verification_token", sa.String(length=255), nullable=True))

    if "verification_token_expires" not in columns:
        op.add_column("users", sa.Column("verification_token_expires", sa.DateTime(), nullable=True))

    if "reset_token" not in columns:
        op.add_column("users", sa.Column("reset_token", sa.String(length=255), nullable=True))

    if "reset_token_expires" not in columns:
        op.add_column("users", sa.Column("reset_token_expires", sa.DateTime(), nullable=True))


def downgrade():
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [col["name"] for col in inspector.get_columns("users")]

    if "reset_token_expires" in columns:
        op.drop_column("users", "reset_token_expires")
    if "reset_token" in columns:
        op.drop_column("users", "reset_token")
    if "verification_token_expires" in columns:
        op.drop_column("users", "verification_token_expires")
    if "verification_token" in columns:
        op.drop_column("users", "verification_token")
