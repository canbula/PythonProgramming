from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a9f2b2fe92f'
down_revision = 'b814c846752b'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('page', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key(batch_op.f('fk_page_user_id_user'), 'user', ['user_id'], ['id'])

def downgrade():
    with op.batch_alter_table('page', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_page_user_id_user'), type_='foreignkey')
        batch_op.drop_column('user_id')
