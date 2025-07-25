"""5. new migration on the remaining apis

Revision ID: 99c95777d060
Revises: 2561e31dd52e
Create Date: 2025-07-10 02:21:52.909258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '99c95777d060'
down_revision = '2561e31dd52e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('balance_sheet_statements', sa.Column('fiscal_year', sa.String(length=4), nullable=False))
    op.drop_column('balance_sheet_statements', 'calendar_year')
    op.add_column('cash_flow_statements', sa.Column('fiscal_year', sa.String(length=4), nullable=False))
    op.drop_column('cash_flow_statements', 'calendar_year')
    op.add_column('revenue_segments', sa.Column('fiscal_Year', sa.Integer(), nullable=False))
    op.drop_column('revenue_segments', 'calendar_year')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('revenue_segments', sa.Column('calendar_year', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('revenue_segments', 'fiscal_Year')
    op.add_column('cash_flow_statements', sa.Column('calendar_year', sa.VARCHAR(length=4), autoincrement=False, nullable=False))
    op.drop_column('cash_flow_statements', 'fiscal_year')
    op.add_column('balance_sheet_statements', sa.Column('calendar_year', sa.VARCHAR(length=4), autoincrement=False, nullable=False))
    op.drop_column('balance_sheet_statements', 'fiscal_year')
    # ### end Alembic commands ###