"""Updated order table

Revision ID: ab4bcaea65e8
Revises: 8c870db51b89
Create Date: 2024-11-12 17:06:37.432369

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'ab4bcaea65e8'
down_revision: Union[str, None] = '8c870db51b89'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order')
    op.drop_index('ix_employee_email', table_name='employee')
    op.drop_table('employee')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('employee',
    sa.Column('id', mysql.CHAR(length=32), nullable=False),
    sa.Column('first_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('last_name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('email', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('department', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.Column('updated_at', mysql.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_employee_email', 'employee', ['email'], unique=True)
    op.create_table('order',
    sa.Column('id', mysql.CHAR(length=32), nullable=False),
    sa.Column('customer_id', mysql.CHAR(length=32), nullable=False),
    sa.Column('amount', mysql.FLOAT(), nullable=False),
    sa.Column('status', mysql.ENUM('PENDING', 'CONFIRMED', 'SHIPPED', 'DELIVERED', 'CANCELLED'), nullable=False),
    sa.Column('order_date', mysql.DATETIME(), nullable=False),
    sa.Column('created_at', mysql.DATETIME(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
