"""My first migration with Alembic

Revision ID: 8614bb018919
Revises: 
Create Date: 2023-07-22 19:16:00.676092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8614bb018919'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('anki_cards', sa.Column('creator_id', sa.Integer(), nullable=True))
    op.add_column('anki_cards', sa.Column('theme_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'anki_cards', 'themes', ['theme_id'], ['id'])
    op.create_foreign_key(None, 'anki_cards', 'users', ['creator_id'], ['id'])
    op.drop_column('anki_cards', 'theme')
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'hashed_password',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.alter_column('users', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.add_column('anki_cards', sa.Column('theme', sa.VARCHAR(length=256), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'anki_cards', type_='foreignkey')
    op.drop_constraint(None, 'anki_cards', type_='foreignkey')
    op.drop_column('anki_cards', 'theme_id')
    op.drop_column('anki_cards', 'creator_id')
    # ### end Alembic commands ###
