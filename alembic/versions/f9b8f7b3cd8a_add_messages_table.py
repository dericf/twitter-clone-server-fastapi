"""add messages_table

Revision ID: f9b8f7b3cd8a
Revises: 809293dcf958
Create Date: 2021-04-27 23:55:17.717957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9b8f7b3cd8a'
down_revision = '809293dcf958'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'messages',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('user_from_id', sa.Integer, sa.ForeignKey(
            "users.id", ondelete="CASCADE"), index=True),
        sa.Column('user_to_id', sa.Integer, sa.ForeignKey(
            "users.id", ondelete="CASCADE"), index=True,),
        sa.Column('content', sa.String),
        sa.Column('is_read', sa.Boolean, default=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.func.now())
    )


def downgrade():
    op.drop_table('messages')
