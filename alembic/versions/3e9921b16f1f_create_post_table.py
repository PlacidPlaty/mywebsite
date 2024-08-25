"""create post table

Revision ID: 3e9921b16f1f
Revises: 
Create Date: 2024-08-25 17:37:25.495769

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3e9921b16f1f'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# handles adding changes
def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key = True),
                    sa.Column('title', sa.String(), nullable = False))
    pass

# handles removal of changes
def downgrade() -> None:
    op.drop_table('posts')
    pass
