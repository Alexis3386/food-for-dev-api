"""Add column user_id in recipe table

Revision ID: 7677ad3a98fd
Revises: 
Create Date: 2024-07-15 18:23:53.694337

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7677ad3a98fd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('recipe', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
    "fk_user_create_recipe",
    "recipe",
    "users",
    ["user_id"],
    ["id"],
)

def downgrade() -> None:
    op.drop_constraint("fk_user_create_recipe", "recipe", "foreignkey")
    op.drop_column('recipe', "user_id")
