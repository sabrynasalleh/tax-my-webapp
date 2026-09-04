"""Change client business relationship

Revision ID: 01081eca0b13
Revises: 4d746c398939
Create Date: 2026-09-04 13:49:55.471026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '01081eca0b13'
down_revision = '4d746c398939'
branch_labels = None
depends_on = None


def upgrade():
    # Create the association table for the many-to-many
    # Business <-> Client relationship
    op.create_table(
        'business_clients',
        sa.Column('business_id', sa.Integer(), nullable=False),
        sa.Column('client_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['business_id'],
            ['businesses.id']
        ),
        sa.ForeignKeyConstraint(
            ['client_id'],
            ['clients.id']
        ),
        sa.PrimaryKeyConstraint('business_id', 'client_id')
    )

    # Copy existing Client -> Business relationships
    # from clients.business_id into the new association table
    op.execute(
        """
        INSERT INTO business_clients (business_id, client_id)
        SELECT business_id, id
        FROM clients
        WHERE business_id IS NOT NULL
        """
    )

    # Remove the old single-business relationship
    # from the clients table
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.drop_column('business_id')


def downgrade():

    # Add the old business_id column back
    with op.batch_alter_table('clients', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'business_id',
                sa.INTEGER(),
                nullable=True
            )
        )

    # Restore one business for each client.
    # Since the old structure only supported one business,
    # only the first association can be restored.
    op.execute(
        """
        UPDATE clients
        SET business_id = (
            SELECT business_id
            FROM business_clients
            WHERE business_clients.client_id = clients.id
            LIMIT 1
        )
        """
    )

    # Remove the many-to-many association table
    op.drop_table('business_clients')