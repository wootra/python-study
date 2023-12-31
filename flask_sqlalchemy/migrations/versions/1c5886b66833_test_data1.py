"""test data1

Revision ID: 1c5886b66833
Revises: fc5d5a954e38
Create Date: 2023-11-19 16:10:47.666650

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "1c5886b66833"
down_revision = "fc5d5a954e38"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "email",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    conn = op.get_bind()
    users = conn.execute(sa.text("select id,email from user")).fetchall()

    emails = [
        {"email": email, "user_id": id, "id": idx}
        for ((id, email), idx) in zip(users, range(len(users)))
    ]
    print("===>", emails)

    # define table representation
    email_table = sa.table(
        "email", sa.column("user_id"), sa.column("email"), sa.column("id")
    )

    # insert records
    op.bulk_insert(email_table, rows=emails)
    # op.bulk_insert(sa.table('email'), rows=emails).commit()

    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.drop_column("email")
    conn.close()
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("user", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                "email", 
                sa.VARCHAR(), 
                nullable=False, 
                server_default="-"
            )
        )

    conn = op.get_bind()
    emails = conn.execute(sa.text("SELECT user_id, email from email"))

    # users = conn.execute(sa.text("select id,email from user")).fetchall()

    for (user_id, email) in emails:
        conn.execute(sa.text(f"update user set email='{email}' where id={user_id}"))
    conn.commit()
    # sa.update("user").where(id=user_id).values(email=email))

    op.drop_table("email")
    # ### end Alembic commands ###
    conn.close()
    