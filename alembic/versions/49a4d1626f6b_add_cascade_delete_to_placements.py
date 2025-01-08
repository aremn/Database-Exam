"""Add cascade delete to placements

Revision ID: 49a4d1626f6b
Revises: 40564dcff3e2
Create Date: 2024-12-28 23:59:21.551780

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '49a4d1626f6b'
down_revision: Union[str, None] = '40564dcff3e2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'placements_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('species_id', sa.Integer, sa.ForeignKey('species.id', ondelete='CASCADE'), nullable=True),
        sa.Column('enclosure_id', sa.Integer, sa.ForeignKey('enclosures.id', ondelete='CASCADE'), nullable=True),
        sa.Column('animal_count', sa.Integer, nullable=False),
    )

    op.execute('INSERT INTO placements_temp (id, species_id, enclosure_id, animal_count) SELECT id, species_id, enclosure_id, animal_count FROM placements')

    op.drop_table('placements')

    op.rename_table('placements_temp', 'placements')

def downgrade():
    op.create_table(
        'placements_temp',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('species_id', sa.Integer, sa.ForeignKey('species.id'), nullable=False),
        sa.Column('enclosure_id', sa.Integer, sa.ForeignKey('enclosures.id'), nullable=False),
        sa.Column('animal_count', sa.Integer, nullable=False),
    )
    op.execute('INSERT INTO placements_temp (id, species_id, enclosure_id, animal_count) SELECT id, species_id, enclosure_id, animal_count FROM placements')
    op.drop_table('placements')
    op.rename_table('placements_temp', 'placements')