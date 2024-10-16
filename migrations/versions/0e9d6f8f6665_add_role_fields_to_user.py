"""Add role fields to User

Revision ID: 0e9d6f8f6665
Revises: 85fcad094aee
Create Date: 2024-10-15 12:55:28.812909

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0e9d6f8f6665"
down_revision = "85fcad094aee"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "role", sa.String(length=50), nullable=False, server_default="user"
            )
        )


def downgrade():
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("role")
