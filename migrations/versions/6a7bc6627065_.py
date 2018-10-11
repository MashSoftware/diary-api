"""empty message

Revision ID: 6a7bc6627065
Revises: e64245435f46
Create Date: 2018-10-11 12:27:51.898538

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6a7bc6627065'
down_revision = 'e64245435f46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('event', sa.Column('change_type', sa.String(), nullable=True))
    op.add_column('event', sa.Column('feed_type', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('event', 'feed_type')
    op.drop_column('event', 'change_type')
    # ### end Alembic commands ###
