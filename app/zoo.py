from alembic import op
import sqlalchemy as sa

revision = 'update_to_zoo_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'species',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('family', sa.String(), nullable=False),
        sa.Column('habitat', sa.String(), nullable=False),
        sa.Column('lifespan', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'enclosures',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('is_indoor', sa.Boolean(), nullable=False),
        sa.Column('area', sa.Float(), nullable=False),
        sa.Column('has_water_source', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'placements',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('species_id', sa.Integer(), nullable=False),
        sa.Column('enclosure_id', sa.Integer(), nullable=False),
        sa.Column('animal_count', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['species_id'], ['species.id'], ),
        sa.ForeignKeyConstraint(['enclosure_id'], ['enclosures.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('placements')
    op.drop_table('enclosures')
    op.drop_table('species')