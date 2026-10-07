"""create audit logs table

Revision ID: 1276dc4944c8
Revises: 619d83d7fb22
Create Date: 2026-10-05 16:35:46.233616

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1276dc4944c8'
down_revision: Union[str, Sequence[str], None] = '619d83d7fb22'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity", sa.String(length=100), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("timestamp", sa.DateTime(timezone=True), nullable=False),
        sa.Column("ip_address", sa.String(length=45), nullable=True),
        sa.Column("log_metadata", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        op.f("ix_audit_logs_id"),
        "audit_logs",
        ["id"],
        unique=False,
    )


def downgrade() -> None:
    pass