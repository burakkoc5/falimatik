"""add birthdate column

Revision ID: xxx
Revises: previous_revision
Create Date: 2024-03-28 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.add_column('users', sa.Column('birthdate', sa.Date(), nullable=True))

def downgrade():
    op.drop_column('users', 'birthdate') 