"""removed bakwas column

Revision ID: b66f4be046be
Revises: 6829325b23ab
Create Date: 2024-05-17 21:19:54.489774

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b66f4be046be'
down_revision = '6829325b23ab'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('bakwas')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bakwas', sa.BOOLEAN(), autoincrement=False, nullable=True))

    # ### end Alembic commands ###