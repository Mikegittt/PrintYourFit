from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('full_name', sa.String(128), nullable=False),
        sa.Column('email', sa.String(128), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(256), nullable=False),
        sa.Column('role', sa.String(32), nullable=False),
        sa.Column('referral_code', sa.String(32), nullable=True, unique=True),
        sa.Column('referred_by', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('target_campus', sa.String(64), nullable=True),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_table(
        'print_shops',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('shop_name', sa.String(128), nullable=False),
        sa.Column('address', sa.Text(), nullable=False),
        sa.Column('state', sa.String(64), nullable=False),
        sa.Column('is_verified', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_table(
        'orders',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('customer_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('print_shop_id', pg.UUID(as_uuid=True), sa.ForeignKey('print_shops.id'), nullable=False),
        sa.Column('referred_by', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('product_type', sa.String(64), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('file_url', sa.Text(), nullable=True),
        sa.Column('design_prompt', sa.Text(), nullable=True),
        sa.Column('unit_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('total_price', sa.Numeric(12, 2), nullable=False),
        sa.Column('status', sa.String(32), server_default='PENDING', nullable=False),
        sa.Column('delivery_address', sa.Text(), nullable=False),
        sa.Column('delivery_fee', sa.Numeric(12, 2), nullable=False),
        sa.Column('payment_reference', sa.String(128), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_table(
        'points_ledger',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('points_delta', sa.Integer(), nullable=False),
        sa.Column('fiat_equivalent', sa.Numeric(12, 2), nullable=False),
        sa.Column('transaction_type', sa.String(32), nullable=False),
        sa.Column('order_id', pg.UUID(as_uuid=True), sa.ForeignKey('orders.id'), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_table(
        'cashout_requests',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('user_id', pg.UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('points_amount', sa.Integer(), nullable=False),
        sa.Column('naira_value', sa.Numeric(12, 2), nullable=False),
        sa.Column('channel', sa.String(32), nullable=False),
        sa.Column('destination', sa.String(128), nullable=False),
        sa.Column('status', sa.String(32), server_default='PENDING', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_table(
        'logistics',
        sa.Column('id', pg.UUID(as_uuid=True), primary_key=True, server_default=sa.text('gen_random_uuid()')),
        sa.Column('order_id', pg.UUID(as_uuid=True), sa.ForeignKey('orders.id'), nullable=False),
        sa.Column('dispatcher_name', sa.String(128), nullable=True),
        sa.Column('tracking_notes', sa.Text(), nullable=True),
        sa.Column('dispatched_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('estimated_delivery', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('delivered_at', sa.TIMESTAMP(timezone=True), nullable=True),
    )

def downgrade():
    op.drop_table('logistics')
    op.drop_table('cashout_requests')
    op.drop_table('points_ledger')
    op.drop_table('orders')
    op.drop_table('print_shops')
    op.drop_table('users')
