from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from models import models, schemas
from database.database import get_db
from models.datatypes import Positions, Teams
from authentication.auth import get_current_league

router = APIRouter(prefix="/players/{league_id}", tags=["Players"])


@router.get("", status_code=status.HTTP_200_OK, response_model=schemas.Players)
async def fetch_players(
    free_agent: bool = False,
    pos: Positions | None = None,
    team: Teams | None = None,
    asc: bool = False,
    skip: int | None = None,
    limit: int | None = None,
    db: AsyncSession = Depends(get_db),
    league: models.League = Depends(get_current_league),
):
    stmt = (
        select(
            models.Player.id,
            models.Player.name,
            models.Player.team,
            models.Player.position,
            models.Player.points_ppr,
            models.Player.points_halfppr,
            models.Player.points_noppr,
            models.TeamPlayer.team_id.label("team_id"),
        )
        .outerjoin(models.TeamPlayer, models.Player.id == models.TeamPlayer.player_id)
        .where(
            or_(
                models.TeamPlayer.team_id.is_(None),
                models.TeamPlayer.league_id == league.id,
            )
        )
    )

    if free_agent:
        stmt = stmt.where(models.TeamPlayer.team_id.is_(None))

    if pos:
        stmt = stmt.where(models.Player.position == pos)

    if team:
        stmt = stmt.where(models.Player.team == team)

    if asc:
        stmt = stmt.order_by(models.Player.points_ppr.asc())
    else:
        stmt = stmt.order_by(models.Player.points_ppr.desc())

    if limit:
        stmt = stmt.limit(limit)

    if skip:
        stmt = stmt.offset(skip)

    players = (await db.execute(stmt)).mappings().all()

    return schemas.Players(
        players=[schemas.PlayersOut.model_validate(player) for player in players]
    )
