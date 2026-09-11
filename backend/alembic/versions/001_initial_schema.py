"""initial schema

Revision ID: 001_initial_schema
Revises: 
Create Date: 2026-07-30

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001_initial_schema'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('framework', sa.String(length=50), nullable=False),
        sa.Column('model_name', sa.String(length=255), nullable=False),
        sa.Column('dataset_path', sa.Text(), nullable=False),
        sa.Column('training_script_path', sa.Text(), nullable=False),
        sa.Column('output_dir', sa.Text(), nullable=False),
        sa.Column('checkpoint_dir', sa.Text(), nullable=False),
        sa.Column('automation_enabled', sa.Boolean(), server_default='true', nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )
    op.create_index('idx_projects_framework', 'projects', ['framework'])

    op.create_table(
        'configurations',
        sa.Column('key', sa.String(length=100), primary_key=True),
        sa.Column('value', postgresql.JSONB(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )

    op.create_table(
        'training_sessions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('projects.id', ondelete='CASCADE'), nullable=False),
        sa.Column('session_name', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False, server_default='INITIALIZING'),
        sa.Column('pid', sa.Integer(), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('exit_code', sa.Integer(), nullable=True),
        sa.Column('hyperparameters', postgresql.JSONB(), server_default='{}'),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('NOW()'), nullable=False)
    )
    op.create_index('idx_sessions_project', 'training_sessions', ['project_id'])

def downgrade() -> None:
    op.drop_table('training_sessions')
    op.drop_table('configurations')
    op.drop_table('projects')
