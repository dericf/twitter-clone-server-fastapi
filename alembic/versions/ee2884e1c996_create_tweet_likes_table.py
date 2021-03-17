"""create tweet_likes table

Revision ID: ee2884e1c996
Revises: 54983669459a
Create Date: 2021-03-17 14:25:31.779045

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee2884e1c996'
down_revision = '54983669459a'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tweet_likes',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('tweet_id', sa.Integer, sa.ForeignKey("tweets.id", ondelete="CASCADE"))
    )


def downgrade():
    op.drop_table('tweet_likes')
