"""Added initial table with changed referral_code fill

Revision ID: ade0277f6a0e
Revises: 42f4a9465248
Create Date: 2024-02-06 19:11:39.014480

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ade0277f6a0e'
down_revision: Union[str, None] = '42f4a9465248'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'referral_code',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=120),
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'referral_code',
               existing_type=sa.String(length=120),
               type_=sa.VARCHAR(length=10),
               existing_nullable=True)
    # ### end Alembic commands ###