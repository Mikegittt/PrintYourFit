from alembic import op
import sqlalchemy as sa

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade():
    # users: add kyc columns
    op.add_column('users', sa.Column('kyc_completed', sa.Boolean(), server_default=sa.text('0'), nullable=False))
    op.add_column('users', sa.Column('kyc_completed_at', sa.DateTime(timezone=True), nullable=True))

    # print_shops: add whatsapp_number, kyc columns, approved_at
    op.add_column('print_shops', sa.Column('whatsapp_number', sa.String(20), nullable=True))
    op.add_column('print_shops', sa.Column('kyc_completed', sa.Boolean(), server_default=sa.text('0'), nullable=False))
    op.add_column('print_shops', sa.Column('kyc_completed_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('print_shops', sa.Column('approved_at', sa.DateTime(timezone=True), nullable=True))

    # notifications table
    op.create_table(
        'notifications',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('title', sa.String(200), nullable=False),
        sa.Column('message', sa.String(2000), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('active', sa.Boolean(), server_default=sa.text('1'), nullable=False),
        sa.Column('source', sa.String(128), nullable=True),
    )


def downgrade():
    op.drop_table('notifications')
    op.drop_column('print_shops', 'approved_at')
    op.drop_column('print_shops', 'kyc_completed_at')
    op.drop_column('print_shops', 'kyc_completed')
    op.drop_column('print_shops', 'whatsapp_number')
    op.drop_column('users', 'kyc_completed_at')
    op.drop_column('users', 'kyc_completed')
