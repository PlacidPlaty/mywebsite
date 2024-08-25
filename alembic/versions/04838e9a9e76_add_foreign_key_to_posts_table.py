"""add foreign key to posts table

Revision ID: 04838e9a9e76
Revises: d5ea0b3801a1
Create Date: 2024-08-25 18:48:51.133985

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '04838e9a9e76'
down_revision: Union[str, None] = 'd5ea0b3801a1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column('owner_id', sa.Integer(), nullable=False))
    # create a foreign key with the users table. name the foreign key: owner_id
    op.create_foreign_key('post_users_fk', source_table = "posts", referent_table = "users",
                          local_cols = ["owner_id"], remote_cols = ['id'], ondelete = "CASCADE")
    pass

# to undo the changes in upgrade
def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name = "posts")
    op.drop_column("posts", "owner_id")
    pass
