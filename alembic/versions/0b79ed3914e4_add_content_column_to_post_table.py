"""add content column to post table

Revision ID: 0b79ed3914e4
Revises: 3e9921b16f1f
Create Date: 2024-08-25 18:02:38.338034

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0b79ed3914e4'
down_revision: Union[str, None] = '3e9921b16f1f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass

# Everytime you set up an upgrade function you have to set a downgrade function.
def downgrade() -> None:
            # <table name>, <column to drop>
    op.drop_column('posts', 'content')
    pass
