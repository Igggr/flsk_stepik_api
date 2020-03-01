"""empty message

Revision ID: af3f2696747b
Revises: 
Create Date: 2020-03-01 13:17:33.771715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'af3f2696747b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('events', sa.Column('_category', sa.Integer(), nullable=True))
    op.add_column('events', sa.Column('_type', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('events', '_type')
    op.drop_column('events', '_category')
    # ### end Alembic commands ###
