"""add user table

Revision ID: d5ea0b3801a1
Revises: 0b79ed3914e4
Create Date: 2024-08-25 18:18:53.293552

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5ea0b3801a1'
down_revision: Union[str, None] = '0b79ed3914e4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable = False),
                    sa.Column('email', sa.String(), nullable = False),
                    sa.Column('password', sa.String(), nullable = False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone = True),
                              server_default=sa.text('now()'), nullable = False),
                    sa.PrimaryKeyConstraint('id'), # set the primary
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
