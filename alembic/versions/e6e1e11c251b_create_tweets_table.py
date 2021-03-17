"""create tweets table

Revision ID: e6e1e11c251b
Revises: 64d575f54bd3
Create Date: 2021-03-16 22:04:34.778473

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e6e1e11c251b'
down_revision = '64d575f54bd3'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tweets',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('content', sa.String, index=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"))
    )

def downgrade():
    op.drop_table('tweets')
