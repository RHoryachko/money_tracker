"""add user_id

Revision ID: add_user_id
Revises: 
Create Date: 2024-04-05 08:55:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_user_id'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('expenses', sa.Column('user_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('expenses', 'user_id') 