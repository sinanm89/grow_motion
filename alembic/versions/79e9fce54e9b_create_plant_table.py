"""create plant table

Revision ID: 79e9fce54e9b
Revises: 
Create Date: 2016-08-17 09:20:26.488272

"""

# revision identifiers, used by Alembic.
revision = '79e9fce54e9b'
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table('plant',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('measured_at', sa.DateTime(timezone=True)),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('ambient_temperature', sa.Integer()),
    sa.Column('ambient_humidity', sa.Float(), nullable=False),
    sa.Column('soil_humidity', sa.Float(), nullable=False),
    ) 


def downgrade():
    op.drop_table('plant')
