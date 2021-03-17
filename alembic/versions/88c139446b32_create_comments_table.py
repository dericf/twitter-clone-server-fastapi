"""create comments table

Revision ID: 88c139446b32
Revises: ee2884e1c996
Create Date: 2021-03-17 14:26:59.875478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '88c139446b32'
down_revision = 'ee2884e1c996'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('tweet_id', sa.Integer, sa.ForeignKey("tweets.id", ondelete="CASCADE")),
        sa.Column('content', sa.String, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('comments')