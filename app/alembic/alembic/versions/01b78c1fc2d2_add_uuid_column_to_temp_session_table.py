"""Add uuid column to temp_session table

Revision ID: 01b78c1fc2d2
Revises: 8614bb018919
Create Date: 2023-08-01 02:11:59.767136

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = "01b78c1fc2d2"
down_revision = "8614bb018919"
branch_labels = None
depends_on = None

# Replace the old UUID definition with a new one using server_default
uuid_server_default = text("uuid_generate_v4()")


# Define the upgrade and downgrade functions
def upgrade():
    op.add_column(
        "temp_session",
        sa.Column(
            "uuid",
            sa.String(),
            unique=True,
            nullable=False,
            server_default=uuid_server_default,
        ),
    )


def downgrade():
    op.drop_column("temp_session", "uuid")
