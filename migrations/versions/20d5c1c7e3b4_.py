"""empty message

Revision ID: 20d5c1c7e3b4
Revises: 6a7bc6627065
Create Date: 2018-10-14 14:20:57.372719

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20d5c1c7e3b4'
down_revision = '6a7bc6627065'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('notes', sa.String(), nullable=True))
    op.drop_column('event', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('description', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('event', 'notes')
    # ### end Alembic commands ###
