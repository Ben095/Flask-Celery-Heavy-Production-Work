"""empty message

Revision ID: 18bf7dc9bb10
Revises: None
Create Date: 2017-01-27 10:47:58.038601

"""

# revision identifiers, used by Alembic.
revision = '18bf7dc9bb10'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Result', sa.Column('search_name', sa.String(length=500), nullable=True))
    op.drop_column('Result', 'query')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Result', sa.Column('query', sa.VARCHAR(length=500), autoincrement=False, nullable=True))
    op.drop_column('Result', 'search_name')
    ### end Alembic commands ###
