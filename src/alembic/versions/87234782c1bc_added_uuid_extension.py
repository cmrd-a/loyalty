"""Added uuid extension

Revision ID: 87234782c1bc
Revises: 
Create Date: 2022-12-25 11:30:41.949118

"""
from alembic import op


# revision identifiers, used by Alembic.
revision = "87234782c1bc"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp" WITH SCHEMA public;')


def downgrade() -> None:
    op.execute('DROP EXTENSION "uuid-ossp";')
