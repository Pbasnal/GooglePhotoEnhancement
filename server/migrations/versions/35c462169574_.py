"""empty message

Revision ID: 35c462169574
Revises: 4b543e8b4030
Create Date: 2022-04-10 15:37:38.385992

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35c462169574'
down_revision = '4b543e8b4030'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photo_album',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('userId', sa.String(length=50), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('productUrl', sa.String(length=200), nullable=False),
    sa.Column('mediaItemsCount', sa.Integer(), nullable=False),
    sa.Column('coverPhotoBaseUrl', sa.String(length=2000), nullable=False),
    sa.Column('coverPhotoMediaItemId', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('photo_album')
    # ### end Alembic commands ###