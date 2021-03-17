"""create user table

Revision ID: 64d575f54bd3
Revises: 
Create Date: 2021-03-16 21:26:48.338701

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '64d575f54bd3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True, nullable=False),
        sa.Column('username', sa.String, index=True),
        sa.Column('bio', sa.String, index=True),
        sa.Column('birthdate', sa.Date, index=True),
        sa.Column('hashed_password', sa.String, nullable=False)
    )



def downgrade():
    op.drop_table('users')