"""create users-tweets relationships

Revision ID: 8bf9f70dbe14
Revises: e6e1e11c251b
Create Date: 2021-03-16 22:07:56.593450

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8bf9f70dbe14'
down_revision = 'e6e1e11c251b'
branch_labels = None
depends_on = None


def upgrade():
    """Since relationships are only defined in SQLAlchemy. This migration version
    is not needed. Skip
    """
    pass


def downgrade():
    """Since relationships are only defined in SQLAlchemy. This migration version
    is not needed. Skip
    """
    pass
