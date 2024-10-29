"""Membuat tabel supplier

Revision ID: 55d5ede1a0c6
Revises: 3f25b8d98c42
Create Date: 2024-10-22 20:44:20.134769

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55d5ede1a0c6'
down_revision = '3f25b8d98c42'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('supplier',
    sa.Column('id_supplier', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('nama_supplier', sa.String(length=250), nullable=False),
    sa.Column('alamat_supplier', sa.Text(), nullable=True),
    sa.Column('telepon_supplier', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id_supplier')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('supplier')
    # ### end Alembic commands ###
