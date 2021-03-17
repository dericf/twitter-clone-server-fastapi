"""create comment_likes table

Revision ID: 809293dcf958
Revises: 88c139446b32
Create Date: 2021-03-17 14:28:19.459816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '809293dcf958'
down_revision = '88c139446b32'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'comment_likes',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column('comment_id', sa.Integer, sa.ForeignKey("comments.id", ondelete="CASCADE")),
    )


def downgrade():
    op.drop_table('comment_likes')