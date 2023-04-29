"""empty message

Revision ID: 7b16e8c61f6e
Revises: 226b9465e06a
Create Date: 2023-04-25 20:29:12.794657

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7b16e8c61f6e'
down_revision = '226b9465e06a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.drop_constraint('_user_post_uc', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('likes', schema=None) as batch_op:
        batch_op.create_unique_constraint('_user_post_uc', ['user_id', 'post_id'])

    # ### end Alembic commands ###
