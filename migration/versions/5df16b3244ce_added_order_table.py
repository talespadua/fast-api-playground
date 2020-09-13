"""added order table

Revision ID: 5df16b3244ce
Revises: 68579e301454
Create Date: 2020-09-12 21:12:38.993546

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5df16b3244ce'
down_revision = '68579e301454'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orders',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('code', sa.Integer(), nullable=False),
    sa.Column('value', sa.Numeric(), nullable=False),
    sa.Column('retailer_document', sa.String(length=30), nullable=False),
    sa.Column('status', sa.String(length=80), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=False),
    sa.Column('cashback', sa.Numeric(), nullable=True),
    sa.ForeignKeyConstraint(['retailer_document'], ['retailers.document'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.alter_column('retailers', 'document',
               existing_type=mysql.VARCHAR(length=30),
               nullable=False)
    op.alter_column('retailers', 'email',
               existing_type=mysql.VARCHAR(length=50),
               nullable=False)
    op.alter_column('retailers', 'full_name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    op.alter_column('retailers', 'password',
               existing_type=mysql.VARCHAR(length=100),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('retailers', 'password',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('retailers', 'full_name',
               existing_type=mysql.VARCHAR(length=100),
               nullable=True)
    op.alter_column('retailers', 'email',
               existing_type=mysql.VARCHAR(length=50),
               nullable=True)
    op.alter_column('retailers', 'document',
               existing_type=mysql.VARCHAR(length=30),
               nullable=True)
    op.drop_table('orders')
    # ### end Alembic commands ###
