from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None


def upgrade():
    # Add status column to print_shops table
    op.add_column('print_shops', sa.Column('status', sa.String(32), server_default='PENDING', nullable=False))
    
    # Add updated_at column to print_shops if it doesn't exist
    op.add_column('print_shops', sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    
    # Create designs table
    op.create_table(
        'designs',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('user_id', sa.String(36), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('prompt', sa.Text(), nullable=False),
        sa.Column('image_url', sa.String(512), nullable=True),
        sa.Column('image_data', sa.LargeBinary(), nullable=True),
        sa.Column('format', sa.String(32), server_default='PNG', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    )


def downgrade():
    op.drop_table('designs')
    op.drop_column('print_shops', 'updated_at')
    op.drop_column('print_shops', 'status')
