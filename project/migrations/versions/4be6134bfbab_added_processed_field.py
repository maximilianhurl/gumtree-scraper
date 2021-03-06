"""Added processed field

Revision ID: 4be6134bfbab
Revises: a70a0d832dd8
Create Date: 2017-11-06 00:02:19.373924

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4be6134bfbab'
down_revision = 'a70a0d832dd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('advert', sa.Column('processed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('advert', 'processed')
    # ### end Alembic commands ###
