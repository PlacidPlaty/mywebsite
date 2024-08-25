"""add more columns to posts

Revision ID: c12e79aecc11
Revises: 04838e9a9e76
Create Date: 2024-08-25 21:14:06.468821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c12e79aecc11'
down_revision: Union[str, None] = '04838e9a9e76'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable = False, server_default = "True"),)
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone= True), nullable = False, 
                            server_default = sa.text ('NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
