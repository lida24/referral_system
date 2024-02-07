"""Change tables

Revision ID: 7a1464dbabc2
Revises: ade0277f6a0e
Create Date: 2024-02-07 17:52:15.992253

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7a1464dbabc2'
down_revision: Union[str, None] = 'ade0277f6a0e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('referral_codes',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('token', sa.String(length=500), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('expiration_date', sa.DateTime(timezone=True), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_table('referrals',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=120), nullable=False),
    sa.Column('referral_code_id', sa.Integer(), nullable=False),
    sa.Column('referrer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['referral_code_id'], ['referral_codes.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['referrer_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.drop_table('access_token')
    op.add_column('users', sa.Column('referral_code_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'users', 'referral_codes', ['referral_code_id'], ['id'], ondelete='SET NULL')
    op.drop_column('users', 'referral_code')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('referral_code', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'users', type_='foreignkey')
    op.drop_column('users', 'referral_code_id')
    op.create_table('access_token',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('token', sa.VARCHAR(length=500), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('expiration_date', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='access_token_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='access_token_pkey'),
    sa.UniqueConstraint('token', name='access_token_token_key')
    )
    op.drop_table('referrals')
    op.drop_table('referral_codes')
    # ### end Alembic commands ###