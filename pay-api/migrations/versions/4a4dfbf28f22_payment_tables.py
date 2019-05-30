"""payment_tables

Revision ID: 4a4dfbf28f22
Revises: daa392b64cb7
Create Date: 2019-05-23 09:14:28.076838

"""
import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision = '4a4dfbf28f22'
down_revision = 'daa392b64cb7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payment_method',
                    sa.Column('code', sa.String(length=10), nullable=False),
                    sa.Column('description', sa.String(length=200), nullable=False),
                    sa.PrimaryKeyConstraint('code')
                    )
    op.create_table('payment_system',
                    sa.Column('code', sa.String(length=10), nullable=False),
                    sa.Column('description', sa.String(length=200), nullable=False),
                    sa.PrimaryKeyConstraint('code')
                    )
    op.create_table('status_code',
                    sa.Column('code', sa.String(length=20), nullable=False),
                    sa.Column('description', sa.String(length=200), nullable=False),
                    sa.PrimaryKeyConstraint('code')
                    )
    op.create_table('payment',
                    sa.Column('created_by', sa.String(length=50), nullable=False),
                    sa.Column('created_on', sa.DateTime(), nullable=False),
                    sa.Column('updated_by', sa.String(length=50), nullable=True),
                    sa.Column('updated_on', sa.DateTime(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('payment_system_code', sa.String(length=10), nullable=False),
                    sa.Column('payment_method_code', sa.String(length=10), nullable=False),
                    sa.Column('payment_status_code', sa.String(length=10), nullable=False),
                    sa.Column('total', sa.Integer(), nullable=False),
                    sa.Column('paid', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['payment_method_code'], ['payment_method.code'], ),
                    sa.ForeignKeyConstraint(['payment_status_code'], ['status_code.code'], ),
                    sa.ForeignKeyConstraint(['payment_system_code'], ['payment_system.code'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('payment_account',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('corp_number', sa.String(length=20), nullable=False),
                    sa.Column('corp_type_code', sa.String(length=10), nullable=False),
                    sa.Column('payment_system_code', sa.String(length=10), nullable=False),
                    sa.Column('account_number', sa.String(length=50), nullable=True),
                    sa.Column('party_number', sa.String(length=50), nullable=True),
                    sa.Column('site_number', sa.String(length=50), nullable=True),
                    sa.ForeignKeyConstraint(['corp_type_code'], ['corp_type.code'], ),
                    sa.ForeignKeyConstraint(['payment_system_code'], ['payment_system.code'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('invoice',
                    sa.Column('created_by', sa.String(length=50), nullable=False),
                    sa.Column('created_on', sa.DateTime(), nullable=False),
                    sa.Column('updated_by', sa.String(length=50), nullable=True),
                    sa.Column('updated_on', sa.DateTime(), nullable=True),
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('payment_id', sa.Integer(), nullable=False),
                    sa.Column('invoice_number', sa.String(length=50), nullable=True),
                    sa.Column('reference_number', sa.String(length=50), nullable=True),
                    sa.Column('invoice_status_code', sa.String(length=10), nullable=False),
                    sa.Column('account_id', sa.Integer(), nullable=False),
                    sa.Column('total', sa.Integer(), nullable=False),
                    sa.Column('paid', sa.Integer(), nullable=True),
                    sa.Column('payment_date', sa.DateTime(), nullable=True),
                    sa.Column('refund', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['account_id'], ['payment_account.id'], ),
                    sa.ForeignKeyConstraint(['invoice_status_code'], ['status_code.code'], ),
                    sa.ForeignKeyConstraint(['payment_id'], ['payment.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('fee_item',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('invoice_id', sa.Integer(), nullable=False),
                    sa.Column('filing_fees', sa.Integer(), nullable=False),
                    sa.Column('fee_schedule_id', sa.Integer(), nullable=False),
                    sa.Column('processing_fees', sa.Integer(), nullable=True),
                    sa.Column('service_fees', sa.Integer(), nullable=True),
                    sa.Column('description', sa.String(length=200), nullable=True),
                    sa.Column('gst', sa.Integer(), nullable=True),
                    sa.Column('pst', sa.Integer(), nullable=True),
                    sa.Column('total', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['fee_schedule_id'], ['fee_schedule.fee_schedule_id'], ),
                    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('payment_line_item',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('invoice_id', sa.Integer(), nullable=False),
                    sa.Column('filing_fees', sa.Integer(), nullable=False),
                    sa.Column('fee_schedule_id', sa.Integer(), nullable=False),
                    sa.Column('quantity', sa.Integer(), nullable=True),
                    sa.Column('processing_fees', sa.Integer(), nullable=True),
                    sa.Column('service_fees', sa.Integer(), nullable=True),
                    sa.Column('description', sa.String(length=200), nullable=True),
                    sa.Column('gst', sa.Integer(), nullable=True),
                    sa.Column('pst', sa.Integer(), nullable=True),
                    sa.Column('total', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['fee_schedule_id'], ['fee_schedule.fee_schedule_id'], ),
                    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('receipt',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('invoice_id', sa.Integer(), nullable=False),
                    sa.Column('receipt_number', sa.String(length=50), nullable=False),
                    sa.Column('receipt_date', sa.DateTime(), nullable=True),
                    sa.Column('receipt_amount', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(['invoice_id'], ['invoice.id'], ),
                    sa.PrimaryKeyConstraint('id')
                    )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('receipt')
    op.drop_table('payment_line_item')
    op.drop_table('fee_item')
    op.drop_table('invoice')
    op.drop_table('payment_account')
    op.drop_table('payment')
    op.drop_table('status_code')
    op.drop_table('payment_system')
    op.drop_table('payment_method')
    # ### end Alembic commands ###
