"""create follows table

Revision ID: 54983669459a
Revises: 8bf9f70dbe14
Create Date: 2021-03-17 14:23:19.751988

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54983669459a'
down_revision = '8bf9f70dbe14'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'follows',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('follows_user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"))
    )


def downgrade():
    op.drop_table('follows')
