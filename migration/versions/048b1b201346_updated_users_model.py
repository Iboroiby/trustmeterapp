"""updated users model

Revision ID: 048b1b201346
Revises: 7624ecdf729c
Create Date: 2025-01-20 17:36:23.561148

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '048b1b201346'
down_revision: Union[str, None] = '7624ecdf729c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_reset_token', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_reset_token')
    # ### end Alembic commands ###
