"""Fix relationships

Revision ID: 3f0a37e4539f
Revises: 49a4d1626f6b
Create Date: 2024-12-29 00:14:17.614038

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3f0a37e4539f'
down_revision: Union[str, None] = '49a4d1626f6b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(op.f('ix_placements_id'), 'placements', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_placements_id'), table_name='placements')
    # ### end Alembic commands ###
