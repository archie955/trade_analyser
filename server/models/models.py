from database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey, UniqueConstraint, Index, Integer, Enum as sqlEnum, DECIMAL
from datetime import datetime
from models.datatypes import Teams, Positions

teamsdt = sqlEnum(Teams, name="teamsdt")
positionsdt = sqlEnum(Positions, name="positionsdt")


class User(Base):
    __tablename__ = "users"

    __table_args__ = (
        Index("ix_users_email", "email"),
        Index("ix_users_username", "username")
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True, 
        autoincrement=True,
        nullable=False
    )
    
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    hashed_password: Mapped[str] = mapped_column(
        String(200),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    leagues = relationship(
        "League",
        back_populates="owner",
        cascade="all, delete-orphan"
        )
    
class League(Base):
    __tablename__ = "leagues"

    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_user_league"),
        Index("ix_leagues_user_id", "user_id")
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )
    
    owner = relationship(
        "User",
        back_populates="leagues"
    )

    teams = relationship(
        "Team",
        back_populates="league",
        cascade="all, delete-orphan"
    )

class Team(Base):
    __tablename__ = "teams"

    __table_args__ = (
        UniqueConstraint("league_id", "name", name="uq_league_team"),
        Index("ix_teams_user_id_league_id", "user_id", "league_id")
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    league_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("leagues.id", ondelete="CASCADE"),
        nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    league = relationship(
        "League",
        back_populates="teams"
    )

    players = relationship(
        "Player",
        secondary="team_players",
        back_populates="teams"
    )

class Player(Base):
    __tablename__ = "players"

    __table_args__ = (
        Index("ix_players_team", "team"),
        Index("ix_players_position", "position"),
        Index("ix_players_points_ppr", "points_ppr"),
        Index("ix_players_points_halfppr", "points_halfppr"),
        Index("ix_players_points_noppr", "points_noppr")
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    team: Mapped[Teams] = mapped_column(
        teamsdt,
        nullable=False
    )
    position: Mapped[Positions] = mapped_column(
        positionsdt,
        nullable=False
    )
    points_ppr: Mapped[float] = mapped_column(
        DECIMAL(10,3),
        nullable=False,
        server_default="0.0"
    )
    points_halfppr: Mapped[float] = mapped_column(
        DECIMAL(10,3),
        nullable=False,
        server_default="0.0"
    )
    points_noppr: Mapped[float] = mapped_column(
        DECIMAL(10,3),
        nullable=False,
        server_default="0.0"
    )

    teams = relationship(
        "Team",
        secondary="team_players",
        back_populates="players"
    )

class TeamPlayer(Base):
    __tablename__ = "team_players"

    __table_args__ = (
        UniqueConstraint("team_id", "player_id", name="uq_team_player"),
        Index("ix_team_players_team_id", "team_id")
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )

    team_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("teams.id", ondelete="CASCADE"),
        nullable=False
    )
    player_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("players.id", ondelete="CASCADE"),
        nullable=True
    )

    team = relationship(
        "Team",
        back_populates="players"
    )
    player = relationship(
        "Player",
        back_populates="teams"
    )



