"""create tables

Revision ID: 69e86df79ef4
Revises: 
Create Date: 2026-04-11 12:17:17.973460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from models.datatypes import Teams, Positions


# revision identifiers, used by Alembic.
revision: str = '69e86df79ef4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    teams_enum = sa.Enum(Teams, name="teamsdt")
    positions_enum = sa.Enum(Positions, name="positionsdt")

    teams_enum.create(op.get_bind(), checkfirst=True)
    positions_enum.create(op.get_bind(), checkfirst=True)

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("email", sa.String(100), nullable=False, unique=True),
        sa.Column("username", sa.String(100), nullable=False, unique=True),
        sa.Column("hashed_password", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_username", "users", ["username"])

    op.create_table(
        "leagues",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.UniqueConstraint("user_id", "name", name="uq_user_league")
    )
    op.create_index("ix_leagues_user_id", "leagues", ["user_id"])

    op.create_table(
        "teams",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("league_id", sa.Integer, sa.ForeignKey("leagues.id", ondelete="CASCADE"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.UniqueConstraint("league_id", "name", name="uq_league_team")
    )
    op.create_index("ix_teams_user_id_league_id", "teams", ["user_id", "league_id"])

    op.create_table(
        "players",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("team", teams_enum, nullable=False),
        sa.Column("position", positions_enum, nullable=False),
        sa.Column("points_ppr", sa.DECIMAL(10, 3), nullable=False, server_default=0.0),
        sa.Column("points_halfppr", sa.DECIMAL(10, 3), nullable=False, server_default=0.0),
        sa.Column("points_noppr", sa.DECIMAL(10, 3), nullable=False, server_default=0.0)
    )
    op.create_index("ix_players_team", "players", ["team"])
    op.create_index("ix_players_position", "players", ["position"])
    op.create_index("ix_players_points_ppr", "players", ["points_ppr"])
    op.create_index("ix_players_points_halfppr", "players", ["points_halfppr"])
    op.create_index("ix_players_points_noppr", "players", ["points_noppr"])

    op.create_table(
        "team_players",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False, autoincrement=True),
        sa.Column("team_id", sa.Integer, sa.ForeignKey("teams.id", ondelete="CASCADE"), nullable=False),
        sa.Column("player_id", sa.Integer, sa.ForeignKey("players.id", ondelete="CASCADE"), nullable=True),
        sa.UniqueConstraint("team_id", "player_id", name="uq_team_player")
    )
    op.create_index("ix_team_players_team_id", "team_players", ["team_id"])


def downgrade():
    op.drop_index("ix_team_players_team_id", table_name="team_players")
    op.drop_table("team_players")
    op.drop_index("ix_players_points_noppr", table_name="players")
    op.drop_index("ix_players_points_halfppr", table_name="players")
    op.drop_index("ix_players_points_ppr", table_name="players")
    op.drop_index("ix_players_position", table_name="players")
    op.drop_index("ix_players_team", table_name="players")
    op.drop_table("players")
    op.drop_index("ix_teams_user_id_league_id", table_name="teams")
    op.drop_table("teams")
    op.drop_index("ix_leagues_user_id", table_name="leagues")
    op.drop_table("leagues")
    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
    
    positions_enum = sa.Enum(name='positionsdt')
    teams_enum = sa.Enum(name='teamsdt')
    positions_enum.drop(op.get_bind(), checkfirst=True)
    teams_enum.drop(op.get_bind(), checkfirst=True)
