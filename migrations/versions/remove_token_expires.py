"""remove verification token expires

Revision ID: [alembic will generate this]
Revises: [previous revision id]
Create Date: [current date]

"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.drop_column('users', 'verification_token_expires')

def downgrade():
    op.add_column('users', sa.Column('verification_token_expires', sa.DateTime(), nullable=True)) 