"""Add column added_date and edit_date to recipe

Revision ID: df99fae8341a
Revises: 7677ad3a98fd
Create Date: 2024-07-16 13:07:37.632016

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df99fae8341a'
down_revision: Union[str, None] = '7677ad3a98fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('recipe', sa.Column('added_date', sa.DateTime(), nullable=True))
    op.add_column('recipe', sa.Column('edit_date', sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column('recipe', 'added_date')
    op.drop_column('recipe', 'edit_date')
